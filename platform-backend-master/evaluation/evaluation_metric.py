from abc import ABC
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score
import json
from sklearn.metrics import f1_score


class BaseMetric(ABC):

    data_type = None

    def compute_metric_by_name(self, metric_name, *args, **kwargs):
        if hasattr(self, metric_name):
            method = getattr(self, metric_name)
            return method(*args, **kwargs)
        else:
            raise ValueError(f'No such metric name: {metric_name}')


class AnomalyDetection(BaseMetric):

    data_type = 'list'

    def __init__(self, y):
        if isinstance(y, str):
            y = json.loads(y)
        self.y_pred = y['y_pred']
        self.y_true = y['y_true']

    def calculate_precision(self):
        correct = sum(1 for true, pred in zip(self.y_true, self.y_pred) if true == pred)
        return correct / len(self.y_true)

    def calculate_recall(self):
        true_positive = sum(1 for true, pred in zip(self.y_true, self.y_pred) if true == pred == 1)
        actual_positive = sum(1 for true in self.y_true if true == 1)
        return true_positive / actual_positive if actual_positive else 0
    
    def calculate_metrics(self, TP, FP, FN):
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        return {
            'precision': format(precision, ".2f"),
            'recall': format(recall, ".2f"),
            'f1_score': format(f1, ".2f")
        }

    # Point-based方法
    def point_based_metrics(self, y_true, y_pred):
        TP = np.sum((y_true == 1) & (y_pred == 1))
        FP = np.sum((y_true == 0) & (y_pred == 1))
        FN = np.sum((y_true == 1) & (y_pred == 0))
        return self.calculate_metrics(TP, FP, FN)

    # Range-based方法
    def range_based_metrics(self, y_true, y_pred, min_length=2):
        y_true_ranges = self.get_ranges(y_true, min_length)
        y_pred_ranges = self.get_ranges(y_pred, min_length)
        
        TP = sum(any(self.overlap(tr, pr) for pr in y_pred_ranges) for tr in y_true_ranges)
        FP = sum(not any(self.overlap(pr, tr) for tr in y_true_ranges) for pr in y_pred_ranges)
        FN = sum(not any(self.overlap(tr, pr) for pr in y_pred_ranges) for tr in y_true_ranges)
        
        return self.calculate_metrics(TP, FP, FN)

    def get_ranges(self, y, min_length):
        ranges = []
        start = None
        for i, val in enumerate(y):
            if val == 1 and start is None:
                start = i
            elif val == 0 and start is not None:
                if i - start >= min_length:
                    ranges.append((start, i))
                start = None
        if start is not None and len(y) - start >= min_length:
            ranges.append((start, len(y)))
        return ranges

    def overlap(self, range1, range2):
        return max(range1[0], range2[0]) < min(range1[1], range2[1])

    # Event-based方法
    def event_based_metrics(self, y_true, y_pred):
        true_events = self.get_events(y_true)
        pred_events = self.get_events(y_pred)
        
        TP = sum(any(pe[0] <= te[1] and pe[1] >= te[0] for pe in pred_events) for te in true_events)
        FP = len(pred_events) - TP
        FN = len(true_events) - TP
        
        return self.calculate_metrics(TP, FP, FN)

    def get_events(self, y):
        events = []
        start = None
        for i, val in enumerate(y):
            if val == 1 and start is None:
                start = i
            elif val == 0 and start is not None:
                events.append((start, i))
                start = None
        if start is not None:
            events.append((start, len(y)))
        return events

    def point_based_f1(self):
        precision = self.calculate_precision()
        recall = self.calculate_recall()
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)
        return {
            'precision': format(precision, ".2f"),
            'recall': format(recall, ".2f"),
            'f1_score': format(f1, ".2f")
        }

    def range_based_f1(self):
        return self.range_based_metrics(self.y_true, self.y_pred)

    def event_based_f1(self):
        return self.event_based_metrics(self.y_true, self.y_pred)


class RootCauseLocalization(BaseMetric):

    data_type = 'dataframe'

    def __init__(self, dataframe):
        """
        Initializes the RootCauseLocalization with a DataFrame.
        DataFrame Columns: top1, top2, top3, top4, top5, groundtruth
        """
        if isinstance(dataframe, str):
            dataframe = pd.read_json(dataframe)
        # Convert column names to lowercase
        dataframe.columns = [col.lower() for col in dataframe.columns]
        self.dataframe = dataframe

    def accuracy_at_k(self, max_k):
        """
        Computes the accuracy@k metric for all k from 1 to max_k, checks if the groundtruth is within the top k predictions.

        Parameters:
        - max_k: int, the maximum top k predictions to consider for accuracy calculation.

        Returns:
        - dict: a dictionary with keys as 'accuracy@k' for each k and values as the computed accuracies.
        """
        accuracy_results = {}

        # Calculate accuracy for each k from 1 to max_k
        for k in range(1, max_k + 1):
            correct_predictions = 0
            # Iterate over each row in the DataFrame
            for _, row in self.dataframe.iterrows():
                # Check if groundtruth is within the top k predictions
                if row['groundtruth'] in row[f'top1':f'top{k}'].values:
                    correct_predictions += 1

            # Calculate accuracy
            total_cases = len(self.dataframe)
            accuracy_at_k = (correct_predictions / total_cases) * 100  # Convert to percentage
            accuracy_results[f'accuracy@{k}'] = accuracy_at_k

        return accuracy_results
    
    def average_accuracy_at_k(self, max_k):
        """
        Computes the average@k metric for all k from 1 to max_k, by averaging the accuracies from 1 to k.

        Parameters:
        - max_k: int, the maximum top k predictions to consider for average calculation.

        Returns:
        - dict: a dictionary with keys as 'average@k' for each k and values as the computed averages.
        """
        accuracy_results = self.accuracy_at_k(max_k)
        average_results = {}

        # Calculate average for each k from 1 to max_k
        for k in range(1, max_k + 1):
            average_at_k = sum(accuracy_results[f'accuracy@{i}'] for i in range(1, k + 1)) / k
            average_results[f'avg@{k}'] = average_at_k

        return average_results

    
    def mean_average_rank(self, df):
        def get_rank(row):
            gt = row['groundtruth']
            for i, col in enumerate(['top1', 'top2', 'top3', 'top4', 'top5']):
                if row[col] == gt:
                    return i + 1
            return 6  # 如果groundtruth不在top5中，则认为rank为6

        ranks = self.dataframe.apply(get_rank, axis=1)
        mar = ranks.mean()
        res_dict = {'mar':mar}
        return res_dict

class FailureClassification(BaseMetric):

    data_type = 'list'

    def __init__(self, y):
        """
        Initializes the FailureClassification with probabilities and true labels.
        - probabilities: A list of lists, where each inner list contains the probabilities for each class for a sample.
        - y_true: A list of actual class labels.
        """
        self.probabilities = np.array(y['probabilities'])
        self.y_true = np.array(y['y_true'])
        self.y_pred = np.argmax(self.probabilities, axis=1)  # Compute predictions from probabilities

    def f1_micro(self):
        """Compute the micro-average precision, recall, and F1-score."""
        precision = precision_score(self.y_true, self.y_pred, average='micro')
        recall = recall_score(self.y_true, self.y_pred, average='micro')
        f1 = f1_score(self.y_true, self.y_pred, average='micro')
        return {
            'precision': format(precision, ".2f"),
            'recall': format(recall, ".2f"),
            'f1_score': format(f1, ".2f")
        }

    def f1_macro(self):
        """Compute the macro-average precision, recall, and F1-score."""
        precision = precision_score(self.y_true, self.y_pred, average='macro')
        recall = recall_score(self.y_true, self.y_pred, average='macro')
        f1 = f1_score(self.y_true, self.y_pred, average='macro')
        return {
            'precision': format(precision, ".2f"),
            'recall': format(recall, ".2f"),
            'f1_score': format(f1, ".2f")
        }

    def f1_weighted(self):
        """Compute the weighted-average precision, recall, and F1-score."""
        precision = precision_score(self.y_true, self.y_pred, average='weighted')
        recall = recall_score(self.y_true, self.y_pred, average='weighted')
        f1 = f1_score(self.y_true, self.y_pred, average='weighted')
        return {
            'precision': format(precision, ".2f"),
            'recall': format(recall, ".2f"),
            'f1_score': format(f1, ".2f")
        }

if __name__ == '__main__':
    # anomaly detection example
    y_true = [1, 0, 1, 1, 0]
    y_pred = [0, 0, 1, 0, 1]
    anomaly = AnomalyDetection(y_true, y_pred)
    print("Point wise f1:", anomaly.compute_metric_by_name('point_wise_f1'))

    # root cause localization example
    # data = {
    #     'top1': ['A', 'B', 'C', 'D', 'E'],
    #     'top2': ['B', 'A', 'D', 'E', 'C'],
    #     'top3': ['C', 'E', 'A', 'B', 'D'],
    #     'top4': ['D', 'D', 'E', 'A', 'A'],
    #     'top5': ['E', 'C', 'B', 'C', 'B'],
    #     'groundtruth': ['A', 'F', 'G', 'F', 'F']
    # }
    # df = pd.DataFrame(data)

    # # Create an instance of RootCauseLocalization
    # rcl = RootCauseLocalization(df)

    # # Compute accuracy@k for k up to 5
    # accuracy_results = rcl.compute_metric_by_name('accuracy_at_k', 5)
    # for key, value in accuracy_results.items():
    #     print(f"{key}: {value}%")

    # failure classification example
    # probabilities = [
    #     [0.7, 0.2, 0.1],
    #     [0.8, 0.3, 0.1],
    #     [0.2, 0.2, 0.6],
    #     [0.8, 0.1, 0.1],
    #     [0.1, 0.4, 0.8],
    #     [0.3, 0.4, 0.3],
    #     [0.3, 0.3, 0.7],
    #     [0.2, 0.6, 0.2],
    #     [0.9, 0.3, 0.6]
    # ]
    # y_true = [0, 1, 2, 0, 1, 1, 0, 1, 2]

    # fc = FailureClassification(probabilities, y_true)
    # print("Micro F1-score:", fc.compute_metric_by_name('f1_micro'))
    # print("Macro F1-score:", fc.compute_metric_by_name('f1_macro'))
    # print("Weighted F1-score:", fc.compute_metric_by_name('f1_weighted'))