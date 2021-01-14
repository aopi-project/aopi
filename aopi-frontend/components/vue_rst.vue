<template>
  <div>
    <div ref="rst">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import rst2html from 'rst2html'
export default {
  name: 'VueRst',
  mounted() {
    const slotData = this.$refs.rst.textContent.trim()
    const htm = rst2html(slotData)
    this.$refs.rst.innerHTML = htm
  },
}
</script>
