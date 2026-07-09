# Tonal - Gerador de Progressões Harmônicas

Um script interativo desenvolvido em **Python** para gerar progressões de acordes aleatórias com base em uma nota tônica. A ferramenta é ideal para músicos, estudantes de teoria musical e produtores buscando inspiração estrutural para novas composições.

O aplicativo roda diretamente no terminal e permite customizar a tonalidade, a complexidade dos acordes e a condução das vozes.

---

## ✨ Funcionalidades

* 🎵 Geração de progressões focadas em escalas maiores e menores naturais
* 🎹 Opção de utilizar tríades básicas ou tétrades (acordes com sétima)
* 🔄 Aplicação de inversões harmônicas, com cálculo automático do baixo na terça ou na quinta
* 🔁 Loop de execução contínuo para sortear várias sequências sem precisar reiniciar o programa

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* Biblioteca nativa Random

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone [https://github.com/lucas-sturiao/tonal.git](https://github.com/lucas-sturiao/tonal.git)
```

```bash
cd Tonal
```

## ▶️ Executando o Projeto

Execute o script principal pelo terminal:

```bash
python main.py
```
Siga as instruções na tela para digitar a tônica, escolher a escala e habilitar tétrades ou inversões.

## 📌 Melhorias Futuras

- [ ] Exportação da progressão para formato MIDI (via biblioteca mido)
- [ ] Transformação do script em uma API RESTful utilizando FastAPI ou Flask
- [ ] Implementação de dominantes secundários e empréstimo modal para criar mais tensão harmônica
- [ ] Sugestão aleatória de BPM e gênero musical (ex: Bossa Nova, Pop, Rock) junto ao sorteio
- [ ] Interface gráfica moderna para substituir a linha de comando

---

## 🤝 Contribuições

Contribuições são sempre bem-vindas!

Caso encontre algum problema ou tenha sugestões de melhorias:

1. Faça um Fork do projeto.
2. Crie uma nova Branch.
3. Faça suas alterações.
4. Envie um Pull Request.