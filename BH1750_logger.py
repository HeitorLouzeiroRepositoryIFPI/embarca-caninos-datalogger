import smbus
import time
from datetime import datetime

# Endereço I2C do BH1750
BH1750_ADDR = 0x23  # ou 0x5C se necessário
I2C_BUS = 2

# Comando para modo contínuo de alta resolução
CONT_H_RES_MODE = 0x10

# Caminho do arquivo de log no microSD
CAMINHO_ARQUIVO = "/media/caninos/8053-D444/luminus/lux_log.txt"

# Inicializa o barramento I2C
bus = smbus.SMBus(I2C_BUS)

def ler_lux():
    try:
        bus.write_byte(BH1750_ADDR, CONT_H_RES_MODE)
        time.sleep(0.2)
        data = bus.read_i2c_block_data(BH1750_ADDR, 0x00, 2)
        raw = (data[0] << 8) | data[1]
        lux = raw / 1.2
        return lux
    except Exception as e:
        print("Erro ao ler BH1750:", e)
        return None

if __name__ == "__main__":
    print("Iniciando leitura e salvamento de luminosidade em .txt...")

    try:
        while True:
            lux = ler_lux()
            if lux is not None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                linha = f"[{timestamp}] Luminosidade: {lux:.2f} lux\n"
                print(linha.strip())

                # Salva no arquivo .txt
                with open(CAMINHO_ARQUIVO, "a") as f:
                    f.write(linha)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nFinalizado.")