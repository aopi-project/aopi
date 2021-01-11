<template>
  <div class="main_bar">
    <v-row align="center" justify="center">
      <v-col>
        <v-switch
          v-model="$vuetify.theme.dark"
          inset
          label="go dark"
        ></v-switch>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'Header',
}
</script>

<style lang="scss" scoped>
.main_bar {
  position: absolute;
  top: 16px;
  right: 16px;
  height: 64px;
}

.v-label {
  display: block ruby !important;
}
</style>
