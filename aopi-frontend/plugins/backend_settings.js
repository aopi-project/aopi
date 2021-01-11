class BackendSettings {
  constructor(settings) {
    this.usersEnabled = settings.users_enabled
  }
}

export default async ({ app }, inject) => {
  const resp = await app.$axios.get('/system')
  const settings = new BackendSettings(resp.data)
  inject('backend_settings', settings)
}
