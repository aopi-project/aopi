<template>
  <div>
    <PluginChecker />
    <v-list flat>
      <v-list-item-group color="primary">
        <v-list-item
          v-for="(item, id) in items"
          :key="item"
          @click="showPackageInfo(id)"
        >
          <v-list-item-avatar>
            <v-img :src="`/languages/${item.language}.svg`"></v-img>
          </v-list-item-avatar>
          <v-list-item-title>
            {{ item.name }}
          </v-list-item-title>
          <v-list-item-content v-if="item.short_description !== null">
            {{ item.short_description }}
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <PackageInfo
      :activator="showPackage"
      :package-info="packageInfo"
      :package-versions="packageVersions"
    ></PackageInfo>
  </div>
</template>

<script>
import PluginChecker from '~/components/plugin_checker'
import PackageInfo from '~/components/package_info'
export default {
  name: 'Packages',
  comments: {
    PluginChecker,
    PackageInfo,
  },
  components: { PluginChecker },
  data() {
    return {
      page: 0,
      items: [],
      limit: 100,
      language: null,
      showPackage: false,
      packageInfo: {},
      packageVersions: [],
      languages: [],
    }
  },
  computed: {
    query() {
      return this.$route.query.q || ''
    },
  },
  async mounted() {
    const response = await this.$axios.get('/packages', {
      params: {
        page: this.page,
        name: this.query,
        limit: this.limit,
        language: this.language,
      },
    })
    this.items = response.data
  },
  methods: {
    async showPackageInfo(value) {
      const packagePreview = this.items[value]
      const packageResponse = await this.$axios.get('/package', {
        params: {
          package_id: packagePreview.id,
          plugin_name: packagePreview.plugin_name,
        },
      })
      this.packageInfo = packageResponse.data
      const versionsResponse = await this.$axios.get('/versions', {
        params: {
          package_id: packagePreview.id,
          plugin_name: packagePreview.plugin_name,
        },
      })
      this.packageVersions = versionsResponse.data
      this.showPackage = true
    },
  },
}
</script>
