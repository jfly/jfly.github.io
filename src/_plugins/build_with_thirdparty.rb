module Jekyll
  Jekyll::Hooks.register :site, :post_write do |site|
    setup_thirdparty(site)
  end

  private

  def self.setup_thirdparty(site)
    destination = site.dest
    photoswipe_source = ENV.fetch("THIRDPARTY_PHOTOSWIPE")

    # Create public directory if it doesn't exist.
    public_dir = File.join(destination, "public")
    FileUtils.mkdir_p(public_dir) unless Dir.exist?(public_dir)

    # Create the symlink.
    photoswipe_link = File.join(public_dir, "photoswipe")

    # Remove existing symlink/directory if it exists.
    if File.exist?(photoswipe_link) || File.symlink?(photoswipe_link)
      File.delete(photoswipe_link)
    end

    # Create new symlink.
    photoswipe_dist = File.join(photoswipe_source, "dist")
    File.symlink(photoswipe_dist, photoswipe_link)

    Jekyll.logger.info "BuildWithThirdparty:", "Created symlink #{photoswipe_link} -> #{photoswipe_dist}"
  end
end
