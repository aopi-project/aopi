export default function ({ $axios }) {
  if (process.client || process.static) {
    const host = window.location.host
    $axios.setBaseURL(`http://${host}/api`)
  }
}
