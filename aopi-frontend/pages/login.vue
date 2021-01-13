<template>
  <v-col class="centered mw-40">
    <v-form ref="form" lazy-validation @submit.prevent="submit_form">
      <v-text-field
        v-model="user.username"
        :error="has_error"
        :error-messages="errors"
        label="Username"
        outlined
        required
        single-line
        @keyup.13="submit_form"
      ></v-text-field>

      <v-text-field
        v-model="user.password"
        :append-icon="show_password ? 'mdi-eye' : 'mdi-eye-off'"
        :error="has_error"
        :error-messages="errors"
        :type="show_password ? 'text' : 'password'"
        label="Password"
        outlined
        required
        single-line
        @keyup.13="submit_form"
        @click:append="show_password = !show_password"
      ></v-text-field>
      <v-row>
        <v-col>
          <v-btn outlined class="w-100" color="warning" @click="reset_form">
            Reset Form
          </v-btn>
        </v-col>
        <v-col>
          <v-btn
            class="w-100"
            color="success"
            outlined
            :loading="logging_in"
            @click="submit_form"
          >
            Submit
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-col>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      show_password: false,
      has_error: false,
      errors: [],
      logging_in: false,
      user: {
        username: null,
        password: null,
      },
    }
  },
  beforeMount() {
    if (this.$auth.loggedIn || !this.$backend_settings.usersEnabled) {
      this.$router.push('/')
    }
  },
  methods: {
    submit_form() {
      this.logging_in = true
      this.has_error = false
      const bodyFormData = new FormData()
      bodyFormData.append('username', this.user.username)
      bodyFormData.append('password', this.user.password)
      this.$auth
        .loginWith('local', {
          data: bodyFormData,
        })
        .then(() => {
          this.$router.push('/')
        })
        .catch((err) => {
          const response = err.response
          if (response.status === 401) {
            this.errors = [response.data.detail]
            this.has_error = true
          }
        })
        .finally(() => (this.logging_in = false))
    },
    reset_form() {
      this.user.username = null
      this.user.password = null
      this.has_error = false
      this.errors = []
      this.show_password = false
    },
  },
}
</script>
