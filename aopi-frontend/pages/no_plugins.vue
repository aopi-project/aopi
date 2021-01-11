<template>
  <div class="centered">
    <h1>Oh, no. Your aopi-server can't work</h1>
    <p>
      We're sorry, but aopi-server was booted without any plugins. To start
      saving your packages install at least one plugin. To do so, install
      plugins using pip package manager.
    </p>
    <div id="termynal" class="h-centered" data-termynal></div>
  </div>
</template>

<script>
import { Termynal } from '~/utils/termynal'

export default {
  name: 'NoPlugins',
  async beforeMount() {
    const response = await this.$axios.get('/languages')
    if (response.data.length > 0) {
      await this.$router.push('/')
    }
  },
  mounted() {
    const term = new Termynal('#termynal', {
      startDelay: 600,
      noInit: true,
      lineData: [
        { type: 'input', value: 'pip install "aopi-python"' },
        { type: 'progress' },
        { delay: 1000, value: 'Successfully installed aopi-python-0.1.22' },
        { type: 'input', value: '# Reboot your aopi-server' },
        { type: 'input', value: 'aopi' },
        { value: 'Now i can run!' },
      ],
    })
    term.init()
  },
}
</script>

<style src="@duckdoc/termynal/termynal.css"></style>

<style scoped>
.h-centered {
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%);
}
</style>
