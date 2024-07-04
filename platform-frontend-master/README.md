# display-frontend

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).



### 前端代码规范

必需：每个vue文件之前；data变量之后；methods内的各方法前；具体说明见下文。

非必需：较复杂方法内需要对方法进行注释，template内元素较多时需要适当的注释以使结构清晰。

#### 必需注释功能及格式说明：

##### 文件注释规范

 单个文件注释规范，每个独立的vue文件开头都要进行注释，表明该文件的描述信息、作者、创建时间等。

```vue
<!--
 * @FileDescription: 该文件的描述信息
 * @Author: 作者信息
 * @Date: 文件创建时间
 * @LastEditors: 最后更新作者
 * @LastEditTime: 最后更新时间
 -->
```



##### 变量的注释

vue文件中data声明的变量的注释。在变量之后简单描述变量的作用。

```vue
count: 0, // 计数器
```



##### 方法注释规范

Vue文件中methods中的方法注释，写于方法前。

```js
 /**
  * @description: 方法描述
  * @param {参数类型} 参数名称
  * @param {参数类型} 参数名称
  * @return 没有返回信息写 void / 有返回信息 {返回类型} 描述信息
  */
```



### 前端调用接口规范

```js
      let params = new URLSearchParams()
      let url = 'display/person/getSearchPersonPageNum'
      params.append('pageSize', 10)
      params.append('category', '不限')
      params.append('searchContent', '')
      this.$http.post(url, params).then((res) => {
        // 调试时可用该语句打印查看后端返回的响应数据
        console.log(res.data)
      })
```



### 注意事项

1、src/components下的文件夹用于存放公用组件，文件夹名为一个单词，文件夹内包含index.vue。
2、src/pages文件夹下的结构与命名方式：文件夹为一个单词，vue文件命名采用PascalName，具体组成为文件夹名+功能名.vue，例如user文件夹下的UserLogin.vue。
3、常用的js函数存放在src/assets/js下。
4、src/network/api下的接口调用函数分业务进行存储，命名方式为业务名+API.js。

5、js文件命名规范：

- 属于类的 `.js` 文件，除 `index.js` 外，使用 `PascalBase` 风格；
- 其他类型的 `.js` 文件，使用 `kebab-case` 风格

6、method 方法命名规范：

- 动宾短语（good：`jumpPage`、`openCarInfoDialog`）（bad：`go`、`nextPage`、`show`、`open`、`login`）
- 接口方法以 `get`、`post` 开头，以 `data` 结尾（good：`getListData`、`postFormData`）（bad：`takeData`、`confirmData`、`getList`、`postForm`）
- 事件方法以 `on` 或者 `handle` 开头（例如：`onTypeChange`、`onUsernameInput`、`handleTypeChange`）
- `init`、`refresh` 单词除外
- 尽量使用常用单词开头（例如`set`、`get`、`open`、`close`、`jump`）
- 驼峰命名（good: `getListData`）（bad: `get_list_data`、`getlistData`）



```
display-frontend
├─ .git
├─ .gitignore
├─ README.md
├─ build
├─ config
├─ index.html
├─ package-lock.json
├─ package.json
├─ postcss.config.js
├─ src
│  ├─ App.vue
│  ├─ assets
│  │  ├─ css 
│  │  ├─ images // 存放静态图片文件
│  │  └─ js
│  │     └─ index.js // 存放常用或可能多次调用的js函数
│  ├─ components // 组件
│  │  ├─ footer
│  │  │  └─ index.vue
│  │  └─ header
│  │     └─ index.vue
│  ├─ main.js
│  ├─ network // 有关发起请求的js文件
│  │  ├─ api // 业务api文件
│  │  │  └─ exampleAPI.js
│  │  └─ axios // axios接口
│  │     └─ index.js
│  ├─ pages // 页面：文件夹为一个单词，vue文件命名采用PascalName
│  │  ├─ index // 索引模块
│  │  │  ├─ IndexKnowledge.vue // 知识索引页
│  │  │  └─ IndexTime.vue // 时间轴索引页
│  │  ├─ knowledge //知识服务模块
│  │  │  ├─ KnowledgeEvent.vue
│  │  │  ├─ KnowledgeLiterature.vue
│  │  │  ├─ KnowledgeMap.vue
│  │  │  ├─ KnowledgeOfficial.vue
│  │  │  ├─ KnowledgeOrganization.vue
│  │  │  ├─ KnowledgePeople.vue
│  │  │  └─ KnowledgePlace.vue
│  │  ├─ permission // 权限管理
│  │  ├─ search // 检索模块
│  │  │  ├─ SearchHome.vue // 检索首页
│  │  │  └─ SearchResult.vue // 检索结果页
│  │  ├─ subject // 专题
│  │  │  ├─ SubjectHome.vue // 专题首页
│  │  │  └─ SubjectDetail.vue // 专题详情
│  │  ├─ user // 用户管理
│  │  │  ├─ UserLogin.vue
│  │  │  └─ UserRegister.vue
│  │  └─ visualization // 可视化模块
│  └─ router // 路由跳转
│     └─ index.js
└─ static
   └─ .gitkeep

```



## vue文件模版

```vue
<template>
  <div></div>
</template>

<script>
  export default {
    components: {},
    data() {
      return {};
    },
    methods: {},
    mounted() {}
  };
</script>

<style scoped>
</style>
```





## 附：组件内部编程规范

### 元素 attribute 顺序

这是 Vue 官方为组件选项推荐的默认顺序。它们被划分为几大类，所以你也能知道新添加的自定义 attribute 和指令应该放到哪里。

- 定义

  （提供组件的选项）  

  - `is`

- 列表渲染

  （创建多个变化的相同元素)

  - `v-for`

- 条件渲染

  （元素是否渲染/显示）

  - `v-if`
  - `v-else-if`
  - `v-else`
  - `v-show`
  - `v-cloak`

- 渲染方式

  （改变元素的渲染方式）

  - `v-pre`
  - `v-once`

- 全局感知

  （需要超越组件的知识）

  - `id`

- 唯一的 attribute

  （需要唯一值的 attribute）

  - `ref`
  - `key`

- 双向绑定

  （把绑定和事件结合起来）

  - `v-model`

- **其它 attribute**（所有普通的绑定或未绑定的 attribute）

- 事件

  （组件事件监听器）

  - `v-on`

- 内容

  （覆写元素的内容）

  - `v-html`
  - `v-text`

注意：不推荐同时使用 `v-if` 和 `v-for`。

### 组件内选项顺序

这是 Vue 官方推荐的组件选项默认顺序。它们被划分为几大类，所以你也能知道从插件里添加的新 property 应该放到哪里。

- 副作用

  （触发组件外的影响）

  - `el`

- 全局感知

  （要求组件以外的知识）

  - `name`
  - `parent`

- 组件类型

  （更改组件的类型）

  - `functional`

- 模板修改器

  （改变模板的编译方式）

  - `delimiters`
  - `comments`

- 模板依赖

  （模板内使用的资源）

  - `components`
  - `directives`
  - `filters`

- 组合

  （向选项里合并 property）

  - `extends`
  - `mixins`

- 接口

  （组件的接口）

  - `inheritAttrs`
  - `model`
  - `props` / `propsData`

- 本地状态

  （本地的响应式 property）

  - `data`
  - `computed`

- 事件

  （通过响应式事件触发的回调）

  - `watch`
  - 生命周期钩子（按照它们被调用的顺序）
    - `beforeCreated`
    - `created`
    - `beforeMount`
    - `mounted`
    - `beforeUpdate`
    - `updated`
    - `activated`
    - `deactivated`
    - `beforeDestroy`
    - `destroyed`

- 非响应式的 property

  （不依赖响应系统的实例 property）

  - `methods`

- 渲染

  （组件输出的声明式描述）

  - `templated` / `render`
  - `renderError`

### prop 名大小写

- 在声明 `prop` 的时候，其命名应该始终使用 `camelCase`。
- 在模板和 JSX 中应该始终使用 `kebab-case`。

子组件

```js
props: {
  myProps: String
}
```

父组件

```js
<my-component :my-props="abc"></my-component>
```

### 自定义事件名

`v-on` 事件监听器在 DOM 模板中会被自动转换为全小写（因为 HTML 是大小写不敏感的），所以 `v-on:myEvent` 将会变成 `v-on:myevent` —— 导致 `myEvent` 不可能被监听到。

因此，应该**始终使用 kebab-case 的事件名**。

子组件

```js
this.$emit('my-event')
```

父组件

```js
<my-component @my-event="abc"></my-component>
```

### data props 方法注意点

- 使用 `data` 里的变量时请先在 `data` 里面初始化；
- `props` 指定类型，也就是 `type`；

### 生命周期方法注意点

- 不在 `mounted`、`created` 之类的方法里直接写取异步数据的逻辑，将方法抽象出来，只在此处调用；
- 在 `created` 里面监听 Bus 事件
