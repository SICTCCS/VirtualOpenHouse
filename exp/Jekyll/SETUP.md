## Setup Required Software to run Jekyll

1. Download and run [RubyInstaller](https://rubyinstaller.org/downloads/) (bold, red link on the left)
2. Click through all defaults; after 'finish', a command prompt will open asking to install additional things. Press enter for the defaults (we want "MSYS2 and MINGW development toolchain")
3. Open a *new command prompt* in *this directory*, run `gem install -g`
4. Check it is installed with `jekyll -v`

Install the 'Liquid' VSCode extension for Jekyll templating syntax support. (it is already configured for HTML files in `.vscode/settings.json`)

## Running

This repo includes a VSCode task

1. In VSCode, click 'Terminal' -> 'Run Task...' -> 'Start Jekyll' (or press enter)
2. Once running, you can press the reload button on the right in your terminal if you want a fresh build (it will reload automatically anyway).

`bundle exec jekyll serve --livereload` is the command if you don't use VSCode. Again, *make sure you're in the correct directory*.

**The directory this runs in has been configured in `.vscode/tasks.json`, you will have to change this if this is moved to the root of the repo.**


***I would recommend the Todo Tree VSCode extension to see all TODO and FIXME comments***
