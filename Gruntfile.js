'use strict';

module.exports = function (grunt) {
    // load all grunt tasks
    require('matchdep').filterAll('grunt-*').forEach(grunt.loadNpmTasks);

    // configurable paths
    var yeomanConfig = {
        app: 'app',
        dist: 'dist',
        local: 'local',
        public: 'static'
    };

    grunt.initConfig({
        yeoman: yeomanConfig,
        watch: {
            coffee: {
                files: ['<%= yeoman.app %>/scripts/**/*.coffee'],
                tasks: ['coffee:watch']
            },
            less: {
                files: ['<%= yeoman.app %>/styles/**/*.less'],
                tasks: ['less:watch', 'copy:watch']
            },
            asset: {
                files: ['<%= yeoman.app %>/assets/**'],
                tasks: ['copy:watch']
            },
        },
        
        bower: {
            options: {
                copy: false,
            },

            install: {
            }
        },

        bower_concat: {
            install: {
                dest: '<%= yeoman.public %>/<%= yeoman.local %>/js/bower.js',
                cssDest: '<%= yeoman.public %>/<%= yeoman.local %>/css/bower.css',
                exclude: ['animate-css', 'font-awesome', 'weather-icons'],
                mainFiles: {
                    'moment': ['../moment.js', '../locale/pl.js'],
                    'jquery-easy-wizard': ['../../lib/jquery.easyWizard.js'],
                    'niftymodals': ['../../js/jquery.modalEffects.js'],
                    'sortable': ['../js/sortable.js']

                },
                callback: function(mainFiles, component) {
                    console.log(component, ":", mainFiles)

                    return mainFiles
                },
                dependencies: {
                    'underscore': 'jquery',
                },
            },

            dist: {
                dest: '<%= yeoman.public %>/<%= yeoman.dist %>/js/bower.js',
                cssDest: '<%= yeoman.public %>/<%= yeoman.dist %>/css/bower.css',
                mainFiles: {
                    'moment': ['../moment.js', '../locale/pl.js'],
                    'jquery-easy-wizard': ['../../lib/jquery.easyWizard.js']
                },
                exclude: ['animate-css', 'font-awesome', 'weather-icons'],
                callback: function(mainFiles, component) {
                    console.log(component, ":", mainFiles)

                    return mainFiles
                },
                dependencies: {
                    'underscore': 'jquery',
                },
            }
        },

        concat: {
            dist: {
                src: ['<%= yeoman.public %>/<%= yeoman.dist %>/js/bower.js', '<%= yeoman.app %>/vendor/lanceng/js/lanceng.js'],
                dest: '<%= yeoman.public %>/<%= yeoman.dist %>/js/plugins.js'
            },
            install: {
                src: ['<%= yeoman.public %>/<%= yeoman.local %>/js/bower.js', '<%= yeoman.app %>/vendor/lanceng/js/lanceng.js'],
                dest: '<%= yeoman.public %>/<%= yeoman.local %>/js/plugins.js'              
            }
        },

        coffee: {
            watch: {
                files: [{
                    expand: true,
                    cwd: '<%= yeoman.app %>/scripts',
                    src: '**/*.coffee',
                    dest: '<%= yeoman.public %>/<%= yeoman.local %>/js',
                    ext: '.js'
                }]
            },
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= yeoman.app %>/scripts',
                    src: '**/*.coffee',
                    dest: '<%= yeoman.public %>/<%= yeoman.dist %>/js',
                    ext: '.js'
                }]
            }
        },
        less: {
            options: {
                strictImports: true,
                paths: [ '<%= yeoman.app %>/styles' ]
            },
            
            watch: {
                options: {
                    dumpLineNumbers: true,
                    compress: false,
                    yuicompress: false,
                    optimization: 2,
                    sourceMap: true,
                    sourceMapFilename: "<%= yeoman.public %>/<%= yeoman.local %>/css/main.css.map",
                    sourceMapBasepath: "<%= yeoman.public %>/<%= yeoman.local %>/css/",
                    outputSourceFiles: true
                },
                files: {
                    '<%= yeoman.public %>/<%= yeoman.local %>/css/main.css': '<%= yeoman.app %>/styles/main.less',
                }
            },

            dist: {
                options: {
                    cleancss: true,
                },
                files: {
                    '<%= yeoman.public %>/<%= yeoman.dist %>/css/main.css': '<%= yeoman.app %>/styles/main.less',
                }
            }
        },
        copy: {
            watch: {
                files: [
                    {expand: true, cwd: '<%= yeoman.app %>/styles', src: ['**.css'], dest: '<%= yeoman.public %>/<%= yeoman.local %>/css'},
                    {expand: true, cwd: '<%= yeoman.app %>/assets', src: ['**'], dest: '<%= yeoman.public %>/<%= yeoman.local %>/assets'},
                ]
            },
            dist: {
                files: [
                    {expand: true, cwd: '<%= yeoman.app %>/styles', src: ['**.css'], dest: '<%= yeoman.public %>/<%= yeoman.dist %>/css'},
                    {expand: true, cwd: '<%= yeoman.app %>/assets', src: ['**'], dest: '<%= yeoman.public %>/<%= yeoman.dist %>/assets'},
                ]
            },
        },
        uglify: {
            install: {
                files: {
                    '<%= yeoman.public %>/<%= yeoman.local %>/js/plugins.min.js': [ '<%= yeoman.public %>/<%= yeoman.local %>/js/plugins.js' ],
                }
            },

            dist: {
                files: [
                    {
                        expand: true, 
                        cwd: '<%= yeoman.public %>/<%= yeoman.dist %>/js', 
                        src: ['**.js', '!**.min.js'], 
                        dest: '<%= yeoman.public %>/<%= yeoman.dist %>/js',
                        ext: '.min.js',
                    },
                ]
            }
        }
    });

    grunt.registerTask('build', [
        'coffee:dist',
        'less:dist',
        'copy:dist',
        'bower_concat:dist',
        'concat:dist',
        'uglify:dist',
    ]);

    grunt.registerTask('install', [
        'bower:install',
        'bower_concat:install',
        'concat:install',
        'uglify:install',
        'coffee:watch',
        'less:watch',
        'copy:watch',
    ])

    grunt.registerTask('distinstall', [
        'install',
        'build',
    ])

    grunt.registerTask('default', 'watch')
};
