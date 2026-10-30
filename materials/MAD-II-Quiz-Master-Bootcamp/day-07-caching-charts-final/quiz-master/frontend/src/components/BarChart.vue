<template>
  <apexchart type="bar" height="280" :options="options" :series="series" />
</template>

<script>
// A small reusable chart:  <BarChart :labels="['Python', 'Web']" :values="[80, 65]" :max="100" />
// <apexchart> is registered once in main.js, so we can use it here without importing it.
// We only describe the chart; <apexchart> draws it.
export default {
  name: 'BarChart',
  props: {
    labels: Array, // names under the bars
    values: Array, // height of each bar
    max: Number, // top of the y axis (100 for percentages), optional
  },
  computed: {
    // the data: one series of bars
    series() {
      return [{ name: 'Value', data: this.values }]
    },
    // how it looks
    options() {
      return {
        chart: { toolbar: { show: false } }, // hide the download menu
        colors: ['#0d6efd'], // Bootstrap blue
        xaxis: { categories: this.labels },
        yaxis: { min: 0, max: this.max, decimalsInFloat: 0 },
      }
    },
  },
}
</script>
