# Smart Email Classifier

## Descrição do Projeto

Sistema inteligente de classificação de emails que utiliza processamento de linguagem natural para categorizar emails em **Produtivo** ou **Improdutivo** e gerar respostas automáticas adequadas para cada categoria.

### Objetivo

Automatizar a leitura e classificação de emails em uma grande empresa do setor financeiro, otimizando o tempo da equipe que anteriormente realizava esse trabalho manualmente.

## Funcionalidades

- **Classificação Inteligente**: Categoriza emails em Produtivo ou Improdutivo usando NLP
- **Upload de Arquivos**: Suporte para arquivos .txt e .pdf
- **Entrada de Texto Direta**: Interface para inserção manual de conteúdo
- **Respostas Automáticas**: Geração de sugestões de resposta baseadas na classificação
- **Interface Responsiva**: Design moderno e adaptável para diferentes dispositivos
- **Processamento Avançado**: Pré-processamento de texto com NLTK e TextBlob

## Tecnologias Utilizadas

### Backend
- **Flask 3.0.3** - Framework web Python
- **TextBlob** - Análise de sentimento e processamento de linguagem natural
- **NLTK** - Processamento de texto e tokenização
- **PyPDF2** - Extração de texto de arquivos PDF
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5/CSS3** - Interface moderna e responsiva
- **JavaScript (ES6+)** - Interatividade e validações do lado cliente
- **Font Awesome** - Biblioteca de ícones
- **CSS Grid/Flexbox** - Sistema de layout responsivo

### Infraestrutura
- **Render** - Plataforma de hospedagem na nuvem (recomendado)
- **Heroku** - Alternativa de hospedagem
- **Git** - Controle de versão

## Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

## Instalação Local

1. **Clone o repositório**
   ```bash
   cd smart_email_classifier
   ```

2. **Crie um ambiente virtual** (recomendado)
   ```bash
   # Windows
   py -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   # Windows
   py -m pip install -r requirements.txt
   
   # Linux/Mac
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   # Windows
   py app.py
   
   # Linux/Mac
   python app.py
   ```

5. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## Como Usar

1. **Acesse a aplicação** através do navegador web
2. **Selecione o método de entrada**:
   - Upload de arquivo (.txt ou .pdf)
   - Inserção direta de texto
3. **Forneça o conteúdo** do email a ser classificado
4. **Execute a classificação** clicando no botão "Classificar Email"
5. **Analise os resultados**:
   - Classificação (Produtivo/Improdutivo)
   - Resposta sugerida
   - Texto original (expandível)
6. **Utilize a resposta** sugerida conforme necessário

## Arquitetura do Sistema

### Algoritmo de Classificação
1. **Pré-processamento**: Remove headers, URLs, endereços de email e caracteres especiais
2. **Análise de Sentimento**: Utiliza TextBlob para determinar a polaridade do texto
3. **Análise de Contexto**: Identifica palavras-chave específicas do ambiente empresarial
4. **Classificação Híbrida**: Combina regras de negócio com análise de sentimento
5. **Pontuação Final**: Algoritmo proprietário determina a classificação final

### Sistema de Pontuação
- **Palavras-chave Produtivas**: +2 pontos cada
- **Palavras-chave Improdutivas**: -1 ponto cada  
- **Sentimento Positivo**: +1 ponto
- **Sentimento Negativo**: +0.5 pontos (problemas requerem ação)
- **Sentimento Neutro**: 0 pontos

### Geração de Resposta
- **Emails Produtivos**: Respostas profissionais indicando análise e próximos passos
- **Emails Improdutivos**: Respostas cordiais de agradecimento e reconhecimento

### Palavras-chave de Classificação

**Contexto Produtivo (Empresarial)**:
- **Urgência**: urgent, deadline, asap, priority, critical
- **Projetos**: project, meeting, status, update, report, analysis
- **Suporte**: question, issue, problem, request, support, help, assistance
- **Ação**: action, proposal, document, review, feedback, decision
- **Financeiro**: budget, cost, revenue, investment, contract, payment

**Contexto Improdutivo (Social/Pessoal)**:
- **Cortesia**: thank you, congratulations, welcome, appreciation
- **Eventos**: birthday, holiday, party, celebration, anniversary
- **Pessoal**: good luck, best wishes, get well, condolences
- **Casual**: weather, weekend, funny, joke, meme, chat

## Estrutura do Projeto

```
smart_email_classifier/
├── app.py                    # Aplicação Flask principal
├── requirements.txt          # Dependências Python
├── Procfile                 # Configuração para Heroku
├── runtime.txt              # Versão específica do Python
├── README.md                # Documentação do projeto
├── app/
│   ├── static/
│   │   ├── favicon.ico      # Ícone da aplicação
│   │   ├── favicon.svg      # Ícone vetorial
│   │   ├── css/
│   │   │   └── style.css    # Estilos CSS
│   │   └── js/
│   │       └── script.js    # JavaScript do frontend
│   └── templates/
│       └── index.html       # Template HTML principal
├── exemplos/
│   └── emails_teste.md      # Casos de teste para validação
├── uploads/                 # Diretório de arquivos temporários
└── Scripts/
```

## Configurações

### Variáveis de Ambiente

- `PORT`: Porta do servidor (padrão: 5000)
- `FLASK_ENV`: Ambiente de execução (development/production)  
- `SECRET_KEY`: Chave secreta do Flask para sessões

### Limitações Técnicas

- **Tamanho máximo de arquivo**: 16MB
- **Formatos suportados**: .txt, .pdf
- **Timeout de processamento**: 30 segundos
- **Codificação de texto**: UTF-8

## Demonstração

- **Aplicação online**: [[Link da aplicação deployada]](https://smart-email-classifier-klm6.onrender.com/)

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request
