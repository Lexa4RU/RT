# Base dorowu Ubuntu desktop + VNC
FROM dorowu/ubuntu-desktop-lxde-vnc:focal

# Remove Chrome repo (known bug)
RUN rm -f /etc/apt/sources.list.d/google-chrome.list

# Update system
RUN apt update && apt upgrade -y

# Install basic cyber tools
RUN apt install -y \
    gnupg wget curl git sudo \
    net-tools iproute2 iputils-ping dnsutils \
    nmap htop tmux build-essential \
    python3 python3-pip python3-venv \
    wireshark tshark \
    xfce4-terminal \
    nano vim \
    openssh-client \
    iperf3 tcpdump netcat-traditional \
    file ltrace strace zsh \
    unzip zip \
    && apt clean

# Install Metasploit from official Rapid7 repo
RUN wget -qO - https://apt.metasploit.com/metasploit-framework.gpg.key | apt-key add - \
    && echo "deb https://apt.metasploit.com/ lucid main" > /etc/apt/sources.list.d/metasploit-framework.list \
    && apt update \
    && apt install -y metasploit-framework

# Install Python pentest tools
RUN pip3 install --no-cache-dir \
    impacket \
    crackmapexec \
    pwntools \
    bloodhound \
    neo4j-driver \
    requests \
    beautifulsoup4 \
    urllib3

# Create a non-root user for VNC session
RUN useradd -m -s /bin/bash pentest \
    && echo "pentest:pentest" | chpasswd \
    && adduser pentest sudo

# Set VNC and default user
ENV USER=pentest
ENV HOME=/home/pentest
WORKDIR /home/pentest

# Set up aliases and bashrc for pentest user
RUN echo 'alias msf="msfconsole"' >> /home/pentest/.bashrc \
    && echo 'alias venom="msfvenom"' >> /home/pentest/.bashrc \
    && echo 'alias cme="crackmapexec"' >> /home/pentest/.bashrc \
    && echo 'alias nb="neo4j"' >> /home/pentest/.bashrc \
    && chown -R pentest:pentest /home/pentest

# Create desktop shortcuts
RUN mkdir -p /home/pentest/Desktop \
    && echo "[Desktop Entry]\nName=Metasploit\nExec=msfconsole\nIcon=utilities-terminal\nType=Application\nTerminal=true" > /home/pentest/Desktop/msf.desktop \
    && echo "[Desktop Entry]\nName=Nmap\nExec=xfce4-terminal -e 'nmap'\nIcon=utilities-terminal\nType=Application\nTerminal=true" > /home/pentest/Desktop/nmap.desktop \
    && echo "[Desktop Entry]\nName=Wireshark\nExec=wireshark\nIcon=network-workgroup\nType=Application\nTerminal=false" > /home/pentest/Desktop/wireshark.desktop \
    && echo "[Desktop Entry]\nName=CrackMapExec\nExec=xfce4-terminal -e 'cme'\nIcon=utilities-terminal\nType=Application\nTerminal=true" > /home/pentest/Desktop/cme.desktop \
    && chown -R pentest:pentest /home/pentest/Desktop \
    && chmod +x /home/pentest/Desktop/*.desktop

# Set default user
USER pentest

# Set default command
CMD ["/bin/bash"]
