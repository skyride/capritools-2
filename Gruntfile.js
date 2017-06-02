module.exports = function (grunt) {

  // Project configuration.
  grunt.initConfig({
    less: {
      options: {
        compress: true,
        sourceMap: true,
        plugins: [
          new (require('less-plugin-clean-css'))({
            'advanced': true,
            'sourceMap': true
          })
        ]
      },
      themes: {
        files: {
          'capritools2/static/capritools2/css/theme-default.min.css': 'capritools2/static/capritools2/less/bootstrap/bootstrap.less',
          'capritools2/static/capritools2/css/theme-flatly.min.css': 'capritools2/static/capritools2/less/theme-flatly/bootstrap.less'
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');

  // Default task
  grunt.registerTask('default', ['less']);
};
