export default {
  name: 'Website Test Report',
  output: './allure-report',
  historyPath: './history.jsonl',
  // appendHistory: false,
  qualityGate: {
    rules: {
      maxFailures: 5,
      fastFail: true,
    },
  },
  plugins: {
    awesome: {
      options: {
        enabled: true,
        reportName: 'Test Report',
        groupBy: ['epic', 'feature', 'story'],
        singleFile: false,
        reportLanguage: 'en',
        open: true,
        publish: true,
      },
    },
  },
  defaultLabels: {
    "severity": "normal",
    "owner": "unassigned",
    "layer": "unknown",
    "tags": ["needs-review"]
  },
  environments: {
    chrome: {
      matcher: ({ labels }) => labels.find(({ name, value }) => name === 'Browser' && value === 'chrome'),
      // variables: {
      //   "Browser": 'chrome',
      //   "Browser.Version": process.env.BROWSER_VERSION || 'latest',
      // },
    },
    safari: {
      matcher: ({ labels }) => labels.find(({ name, value }) => name === 'Browser' && value === 'safari'),
    },
    firefox: {
      matcher: ({ labels }) => labels.find(({ name, value }) => name === 'Browser' && value === 'firefox'),
    },
  },
}