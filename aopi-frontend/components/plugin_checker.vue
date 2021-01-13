<template>
  <div class="plugin_checker"></div>
</template>

<script>
export default {
  name: 'PluginChecker',
  async beforeMount() {
    if (this.$backend_settings.usersEnabled && !this.$auth.loggedIn) {
      await this.$router.push('/login')
    }
    const response = await this.$axios.get('/languages')
    if (response.data.length < 1) {
      await this.$router.push('/no_plugins')
    }
  },
}
</script>
