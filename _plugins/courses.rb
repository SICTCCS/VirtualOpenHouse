module CoursePlugin
  class CoursePageGenerator < Jekyll::Generator
    safe true

    def generate(site)
      # Loop through _courses collection
      site.collections['courses'].docs.each do |course|
        # Create 3 virtual pages: course, classroom, teacher
        ['course', 'classroom', 'teacher'].each do |type|
          site.pages << CoursePage.new(site, course, type)
        end
      end
    end
  end

  class CoursePage < Jekyll::Page
    def initialize(site, course, type)
      @site = site
      @base = site.source
      # Set URL structure: ex: /math101/teacher/index.html
      @dir  = File.join(type, course.data['slug'] || course.basename_without_ext)
      @name = 'index.html'

      self.process(@name)
      # Link layout page type
      self.read_yaml(File.join(@base, '_layouts'), "#{type}.html")
      
      # Pass all data from course file to virtual page
      self.data.merge!(course.data)
      self.data['type'] = type
    end
  end
end