## Installation Process

### Creating Environment

1. **Install asdf** 
   Follow the instructions at [asdf-vm](https://asdf-vm.com/manage/plugins.html).

2. **Run the following commands:**

   ```bash
   # Install asdf (if not already installed)
   git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.11.3
   echo -e '\n. $HOME/.asdf/asdf.sh' >> ~/.bashrc
   echo -e '\n. $HOME/.asdf/completions/asdf.bash' >> ~/.bashrc
   source ~/.bashrc

3. **Install asdf Ruby plugin:**

    ```bash
    asdf plugin-add ruby https://github.com/asdf-vm/asdf-ruby.git
    ```

4. **Install dependencies:**

    ```bash
    sudo apt-get update
    sudo apt-get install -y autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm6 libgdbm-dev
    ```
5. **Install Ruby 2.5.3:**

    ```bash
    asdf install ruby 2.5.3
    ```

6. **Set Ruby 2.5.3 as the global version:**

    ```bash
    asdf global ruby 2.5.3
    ```

7. **Create the database:**

    ```bash
    rake db:create
    ```

8. **Migrate the database:**

    ```bash
    rake db:migrate
    ```

9. **Merge the created database with the dump (as there are no seeds in app/assets/*.csv):**
    - Follow your standard procedure for merging database dumps.

10. **Run the Rails server:**
    ```bash
    rails s
    ```