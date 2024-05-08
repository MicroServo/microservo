# OnlineBoutique
if [ ! -d helm-chart ] ; then
    cd ..
fi

# remove old images
minikube image ls | grep psy7604 | xargs -i sh -c "minikube image rm -v=1 {}"

# load new images
minikube image load $(docker image ls | grep psy7604 | awk '{print $1 ":" $2}')

# bash doc_addons/4.create_ob.sh
helm install onlineboutique ./helm-chart

cd doc_addons
