<template>
  <div id="home">
    <img class="mt-3 spin" src="../assets/logo.png">
  </div>
</template>

<style>
img.spin{
    animation: rotate_image 10s linear infinite;
    transform-origin: 50% 50%;
}

@keyframes rotate_image{
  100% {
    transform: rotate(360deg);
  }
}
</style>
