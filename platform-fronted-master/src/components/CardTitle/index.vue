<template>
  <div class="card-title">
    <span><slot /></span>
  </div>
</template>

<script>
export default {

}
</script>

<style>
.card-title {
  position: relative;
  text-align: left;
  font-weight: bold;
  margin-bottom: 5px;
}
.card-title::before {
  display: inline-block;
  content: ' ';
  width: 2px;
  height: 16px;
  border-left: 2px solid #00A0FF;
  position: absolute;
  left: 0;
  top: -50%;
  transform: translateX(-5px) translateY(100%);
}
.card-title > span {
  margin-left: 5px;
}
</style>
