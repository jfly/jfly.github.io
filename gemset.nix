{
  addressable = {
    dependencies = [ "public_suffix" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0cl2qpvwiffym62z991ynks7imsm87qmgxf0yfsmlwzkgi9qcaa6";
      type = "gem";
    };
    version = "2.8.7";
  };
  colorator = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0f7wvpam948cglrciyqd798gdc6z3cfijciavd0dfixgaypmvy72";
      type = "gem";
    };
    version = "1.1.0";
  };
  concurrent-ruby = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1ipbrgvf0pp6zxdk5ascp6i29aybz2bx9wdrlchjmpx6mhvkwfw1";
      type = "gem";
    };
    version = "1.3.5";
  };
  csv = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0gz7r2kazwwwyrwi95hbnhy54kwkfac5swh2gy5p5vw36fn38lbf";
      type = "gem";
    };
    version = "3.3.5";
  };
  em-websocket = {
    dependencies = [
      "eventmachine"
      "http_parser.rb"
    ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1a66b0kjk6jx7pai9gc7i27zd0a128gy73nmas98gjz6wjyr4spm";
      type = "gem";
    };
    version = "0.5.3";
  };
  eventmachine = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0wh9aqb0skz80fhfn66lbpr4f86ya2z5rx6gm5xlfhd05bj1ch4r";
      type = "gem";
    };
    version = "1.2.7";
  };
  ffi = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "19kdyjg3kv7x0ad4xsd4swy5izsbb1vl1rpb6qqcqisr5s23awi9";
      type = "gem";
    };
    version = "1.17.2";
  };
  forwardable-extended = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "15zcqfxfvsnprwm8agia85x64vjzr2w0xn9vxfnxzgcv8s699v0v";
      type = "gem";
    };
    version = "2.6.0";
  };
  "http_parser.rb" = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1gj4fmls0mf52dlr928gaq0c0cb0m3aqa9kaa6l0ikl2zbqk42as";
      type = "gem";
    };
    version = "0.8.0";
  };
  i18n = {
    dependencies = [ "concurrent-ruby" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "03sx3ahz1v5kbqjwxj48msw3maplpp2iyzs22l4jrzrqh4zmgfnf";
      type = "gem";
    };
    version = "1.14.7";
  };
  jekyll = {
    dependencies = [
      "addressable"
      "colorator"
      "csv"
      "em-websocket"
      "i18n"
      "jekyll-sass-converter"
      "jekyll-watch"
      "kramdown"
      "liquid"
      "mercenary"
      "pathutil"
      "rouge"
      "safe_yaml"
      "webrick"
    ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "144dvgqffkkp34763hj0wh1qabd0fq22sx7bk7afgpy73mv3n8f4";
      type = "gem";
    };
    version = "3.10.0";
  };
  jekyll-paginate = {
    groups = [ "jekyll_plugins" ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0r7bcs8fq98zldih4787zk5i9w24nz5wa26m84ssja95n3sas2l8";
      type = "gem";
    };
    version = "1.1.0";
  };
  jekyll-sass-converter = {
    dependencies = [ "sass" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "008ikh5fk0n6ri54mylcl8jn0mq8p2nfyfqif2q3pp0lwilkcxsk";
      type = "gem";
    };
    version = "1.5.2";
  };
  jekyll-watch = {
    dependencies = [ "listen" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1qd7hy1kl87fl7l0frw5qbn22x7ayfzlv9a5ca1m59g0ym1ysi5w";
      type = "gem";
    };
    version = "2.2.1";
  };
  kramdown = {
    dependencies = [ "rexml" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1ic14hdcqxn821dvzki99zhmcy130yhv5fqfffkcf87asv5mnbmn";
      type = "gem";
    };
    version = "2.4.0";
  };
  kramdown-parser-gfm = {
    dependencies = [ "kramdown" ];
    groups = [ "jekyll_plugins" ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0a8pb3v951f4x7h968rqfsa19c8arz21zw1vaj42jza22rap8fgv";
      type = "gem";
    };
    version = "1.1.0";
  };
  liquid = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1czxv2i1gv3k7hxnrgfjb0z8khz74l4pmfwd70c7kr25l2qypksg";
      type = "gem";
    };
    version = "4.0.4";
  };
  listen = {
    dependencies = [
      "rb-fsevent"
      "rb-inotify"
    ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0rwwsmvq79qwzl6324yc53py02kbrcww35si720490z5w0j497nv";
      type = "gem";
    };
    version = "3.9.0";
  };
  mercenary = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "10la0xw82dh5mqab8bl0dk21zld63cqxb1g16fk8cb39ylc4n21a";
      type = "gem";
    };
    version = "0.3.6";
  };
  pathutil = {
    dependencies = [ "forwardable-extended" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "12fm93ljw9fbxmv2krki5k5wkvr7560qy8p4spvb9jiiaqv78fz4";
      type = "gem";
    };
    version = "0.16.2";
  };
  public_suffix = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1vb6f3v8q9m67xmbdl4vbmxis53a7igci4blg561jdfp613cf3i5";
      type = "gem";
    };
    version = "5.1.1";
  };
  rb-fsevent = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1zmf31rnpm8553lqwibvv3kkx0v7majm1f341xbxc0bk5sbhp423";
      type = "gem";
    };
    version = "0.11.2";
  };
  rb-inotify = {
    dependencies = [ "ffi" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0vmy8xgahixcz6hzwy4zdcyn2y6d6ri8dqv5xccgzc1r292019x0";
      type = "gem";
    };
    version = "0.11.1";
  };
  rexml = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0hninnbvqd2pn40h863lbrn9p11gvdxp928izkag5ysx8b1s5q0r";
      type = "gem";
    };
    version = "3.4.4";
  };
  rouge = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "1dnfkrk8xx2m8r3r9m2p5xcq57viznyc09k7r3i4jbm758i57lx3";
      type = "gem";
    };
    version = "3.30.0";
  };
  safe_yaml = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0j7qv63p0vqcd838i2iy2f76c3dgwzkiz1d1xkg7n0pbnxj2vb56";
      type = "gem";
    };
    version = "1.0.5";
  };
  sass = {
    dependencies = [ "sass-listen" ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0p95lhs0jza5l7hqci1isflxakz83xkj97lkvxl919is0lwhv2w0";
      type = "gem";
    };
    version = "3.7.4";
  };
  sass-listen = {
    dependencies = [
      "rb-fsevent"
      "rb-inotify"
    ];
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "0xw3q46cmahkgyldid5hwyiwacp590zj2vmswlll68ryvmvcp7df";
      type = "gem";
    };
    version = "4.0.0";
  };
  webrick = {
    groups = [
      "default"
      "jekyll_plugins"
    ];
    platforms = [ ];
    source = {
      remotes = [ "https://rubygems.org" ];
      sha256 = "12d9n8hll67j737ym2zw4v23cn4vxyfkb6vyv1rzpwv6y6a3qbdl";
      type = "gem";
    };
    version = "1.9.1";
  };
}
