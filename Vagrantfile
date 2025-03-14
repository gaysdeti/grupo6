Vagrant.configure("2") do |config|
    # VM Gerador de Dados
    config.vm.define "gerador_dados" do |gerador|
      gerador.vm.box = "ubuntu/focal64"
      gerador.vm.hostname = "gerador-dados"
      gerador.vm.network "private_network", ip: "192.168.56.10"
      gerador.vm.provision "shell", path: "provisionamento/gerador/install.sh"
      gerador.vm.provision "shell", path: "scripts/gerador.py"
    end
  
    # VM Banco de Dados
    config.vm.define "banco_dados" do |banco|
      banco.vm.box = "ubuntu/focal64"
      banco.vm.hostname = "banco-dados"
      banco.vm.network "private_network", ip: "192.168.56.20"
      banco.vm.provision "shell", path: "provisionamento/banco/install.sh"
      banco.vm.provision "shell", path: "scripts/setup_banco_dados.sh"
    end
  
    # VM Microserviço
    config.vm.define "microservico" do |micro|
      micro.vm.box = "ubuntu/focal64"
      micro.vm.hostname = "microservico"
      micro.vm.network "private_network", ip: "192.168.56.30"
      micro.vm.provision "shell", path: "provisionamento/microservico/install.sh"
      micro.vm.provision "shell", path: "scripts/setup_microservico.sh"
    end
  end  