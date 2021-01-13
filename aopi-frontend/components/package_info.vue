<template>
  <v-dialog
    v-model="activator"
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition"
  >
    <v-card>
      <v-toolbar color="primary" dark>
        <v-btn dark icon @click="activator = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>{{ packageInfo.name }}</v-toolbar-title>
      </v-toolbar>
      <v-row class="mt-3 ml-1 mr-1">
        <v-col>
          <h2>Package Description</h2>
          <div
            v-if="
              packageInfo.description === null ||
              packageInfo.description.trim().length === 0
            "
          >
            No description provided
          </div>
          <pre v-else>
 {{ packageInfo.description }}
          </pre>
        </v-col>
        <v-col>
          <h2>Package versions</h2>
          <v-expansion-panels inset>
            <v-expansion-panel
              v-for="version in packageVersions"
              :key="version"
            >
              <v-expansion-panel-header
                v-if="version.yanked === true"
                disable-icon-rotate
              >
                <template v-slot:actions>
                  <v-icon color="error"> mdi-alert-circle</v-icon>
                </template>
                {{ version.version }}
              </v-expansion-panel-header>
              <v-expansion-panel-header v-else>
                {{ version.version }}
              </v-expansion-panel-header>

              <v-expansion-panel-content>
                <v-banner v-if="version.yanked === true" two-line>
                  <v-avatar slot="icon" color="red accent-4" size="40">
                    <v-icon color="white" icon="mdi-skull-scan">
                      mdi-skull-scan
                    </v-icon>
                  </v-avatar>
                  This version was yanked
                </v-banner>
                <h3>Version info</h3>
                <p
                  v-for="(property, name) in filtered_metadata(
                    version.metadata
                  )"
                  :key="property"
                >
                  {{ name }}: {{ property }}
                </p>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'PackageInfo',
  props: {
    activator: { type: Boolean, required: true },
    packageInfo: {
      type: Object,
      default: null,
    },
    packageVersions: {
      type: Array,
      default: () => {
        return []
      },
    },
  },
  methods: {
    filtered_metadata(rawMetadata) {
      const newMeta = {}
      for (const item in rawMetadata) {
        if (rawMetadata[item] !== null) {
          newMeta[item] = rawMetadata[item]
        }
      }
      return newMeta
    },
  },
}
</script>
