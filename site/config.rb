activate :deploy do |deploy|
  deploy.method = :git
  # Optional Settings
  # deploy.remote   = 'custom-remote' # remote name or git url, default: origin
  # deploy.branch   = 'custom-branch' # default: gh-pages
  # deploy.strategy = :submodule      # commit strategy: can be :force_push or :submodule, default: :force_push
  # deploy.commit_message = 'custom-message'      # commit message (can be empty), default: Automated commit at `timestamp` by middleman-deploy `version`
end

configure :development do
  set :site_url, "http://localhost:4567"
end

set :css_dir, 'stylesheets'

set :js_dir, 'javascripts'

set :images_dir, 'images'

# Build-specific configuration
configure :build do
  set :site_url, "http://rackerlabs.github.io/wadl2swagger"

  # For example, change the Compass output style for deployment
  activate :minify_css

  # Minify Javascript on build
  activate :minify_javascript

  # Enable cache buster
  # activate :cache_buster

  # Use relative URLs
  activate :relative_assets

  # Compress PNGs after build
  # First: gem install middleman-smusher
  # require "middleman-smusher"
  # activate :smusher

  # Or use a different image path
  # set :http_path, "/Content/images/"

  set :build_dir, './build'
end

helpers do
  def swagger_validation_image(log_file)
    validation_result = File.read(log_file.source_file.lines[-1])
    case validation_result
    when /Invalid/
      url_for "images/invalid.png"
    when /Valid/
      url_for "images/valid.png"
    else
      url_for "images/error.png"
    end
  end
end
