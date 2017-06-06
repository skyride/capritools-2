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
          'capritools2/static/capritools2/css/theme-flatly.min.css': 'capritools2/static/capritools2/less/theme-flatly/bootstrap.less',
          'capritools2/static/capritools2/css/theme-darkly.min.css': 'capritools2/static/capritools2/less/theme-darkly/bootstrap.less',
          'capritools2/static/capritools2/css/theme-cyborg.min.css': 'capritools2/static/capritools2/less/theme-cyborg/bootstrap.less',
          'capritools2/static/capritools2/css/theme-lumen.min.css': 'capritools2/static/capritools2/less/theme-lumen/bootstrap.less',
          'capritools2/static/capritools2/css/theme-slate.min.css': 'capritools2/static/capritools2/less/theme-slate/bootstrap.less',
          'capritools2/static/capritools2/css/theme-solar.min.css': 'capritools2/static/capritools2/less/theme-solar/bootstrap.less',
          'capritools2/static/capritools2/css/theme-yeti.min.css': 'capritools2/static/capritools2/less/theme-yeti/bootstrap.less',
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');

  // Default task
  grunt.registerTask('default', ['less']);
};
