<template>
  <div class="centered">
    <v-row justify="center" align-content="center">
      <template>
        <v-col v-for="tab in control_tabs" :key="tab">
          <v-hover v-slot="{ hover }">
            <div>
              <v-card
                class="mx-auto flex-center"
                min-height="250"
                min-width="250"
                max-width="344"
                outlined
                @hover="hover = !hover"
              >
                <v-icon
                  dense
                  style="font-size: 120px"
                  class="fill-height flex-column"
                >
                  {{ tab.icon }}
                </v-icon>
                <v-expand-transition mode="out-in">
                  <v-overlay v-if="hover" absolute color="#1976D2">
                    <v-btn :href="tab.to">{{ tab.title }}</v-btn>
                  </v-overlay>
                </v-expand-transition>
              </v-card>
            </div>
          </v-hover>
        </v-col>
      </template>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'Index',
  data() {
    return {
      control_tabs: [
        {
          title: 'manage users',
          icon: 'mdi-account',
          to: '/admin/users',
        },
        {
          title: 'manage groups',
          icon: 'mdi-account-multiple',
          to: '/admin/groups',
        },
        {
          title: 'manage packages',
          icon: 'mdi-package-variant',
          to: '/admin/packages',
        },
      ],
    }
  },
}
</script>

<style lang="scss">
.flex-center {
  display: flex !important;
  justify-content: center;
}

.text-center {
  text-align: center;
}
</style>
