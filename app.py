from flask import Flask, request, render_template, jsonify
import os
import PyPDF2
import re
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class EmailClassifier:
    def __init__(self):
        self.productive_keywords = [
            'urgente', 'prazo', 'deadline', 'projeto', 'reunião', 'relatório', 
            'status', 'atualização', 'pergunta', 'questão', 'dúvida', 'problema', 
            'solicitação', 'pedido', 'suporte', 'ajuda', 'ação', 'proposta', 
            'documento', 'revisão', 'feedback', 'cronograma', 'orçamento', 
            'tarefa', 'entrega', 'marco', 'requisito', 'especificação', 'análise',
            'solução', 'implementação', 'desenvolvimento', 'teste', 'aprovação',
            'decisão', 'prioridade', 'crítico', 'importante', 'necessário',
            'preciso', 'podem', 'aguardo', 'retorno', 'esclarecimento',
            'informação', 'dados', 'validação', 'definição', 'quando', 'como',
            
            'urgent', 'deadline', 'project', 'meeting', 'report', 'status', 
            'update', 'question', 'issue', 'problem', 'request', 'support', 
            'help', 'action', 'proposal', 'document', 'review', 'feedback', 
            'schedule', 'budget', 'task', 'deliverable', 'milestone', 
            'requirement', 'specification', 'analysis', 'solution', 
            'implementation', 'development', 'testing', 'approval', 
            'decision', 'priority', 'critical', 'important', 'asap'
        ]
        
        self.unproductive_keywords = [
            'parabéns', 'feliz', 'aniversário', 'natal', 'ano novo', 'feriado',
            'obrigado', 'obrigada', 'agradecimento', 'abraços', 'beijos', 'carinho',
            'final de semana', 'descansar', 'família', 'diversão', 'alegrar',
            'piada', 'humor', 'risada', 'felicidade', 'paz', 'amor', 'amizade',
            'especial', 'maravilhoso', 'excelente', 'ótimo', 'lindo', 'perfeito',
            'bom dia', 'boa tarde', 'boa noite', 'boa semana', 'bom final',
            'nos vemos', 'até logo', 'pessoal', 'galera', 'queridos', 'colegas',
            'equipe', 'time', 'todos', 'conquistas', 'alegrias', 'próspero',
            'saúde', 'sorte', 'incrível', 'reconfortante', 'torcendo', 'apoio',
            'passeio', 'parque', 'tempo', 'curtir', 'aproveitem', 'desejo',
            
            'congratulations', 'happy', 'birthday', 'christmas', 'new year',
            'thanks', 'thank you', 'greeting', 'weekend', 'holiday', 'vacation',
            'family', 'fun', 'joke', 'humor', 'laugh', 'happiness', 'peace', 
            'love', 'friendship', 'wonderful', 'excellent', 'great', 'amazing',
            'good morning', 'good afternoon', 'good night', 'good week',
            'bye', 'see you', 'folks', 'team', 'everyone', 'wishes', 'enjoy'
        ]
        
        logger.info("Email classifier initialized successfully with rule-based approach")
    
    def preprocess_text(self, text):
        if not text:
            return ""
            
        text_lower = text.lower()
        text_lower = re.sub(r'^(from:|to:|subject:|date:|cc:|bcc:).*$', '', text_lower, flags=re.MULTILINE)
        text_lower = re.sub(r'http[s]?://\S+', '', text_lower)
        text_lower = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text_lower)
        text_lower = re.sub(r'\s+', ' ', text_lower).strip()
        return text_lower
    
    def analyze_sentiment(self, text):
        if not text:
            return 0.0
            
        positive_words = ['bom', 'boa', 'excelente', 'ótimo', 'feliz', 'alegria', 'amor', 'paz', 'maravilhoso', 'incrível', 'perfeito', 'great', 'excellent', 'wonderful', 'amazing', 'perfect', 'happy', 'love', 'peace']
        negative_words = ['problema', 'erro', 'crítico', 'urgente', 'falha', 'bug', 'issue', 'error', 'problem', 'critical', 'urgent', 'fail']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if any(pos in word for pos in positive_words))
        negative_count = sum(1 for word in words if any(neg in word for neg in negative_words))
        
        if positive_count + negative_count == 0:
            return 0.0
            
        sentiment = (positive_count - negative_count) / (positive_count + negative_count)
        return sentiment
    
    def classify_email(self, text):
        if not text or not text.strip():
            return "Produtivo"
            
        processed_text = self.preprocess_text(text)
        original_text_lower = text.lower()
        
        productive_score = sum(1 for keyword in self.productive_keywords if keyword in processed_text)
        unproductive_score = sum(1 for keyword in self.unproductive_keywords if keyword in processed_text)
        
        sentiment = self.analyze_sentiment(processed_text)
        
        has_question = '?' in text or any(word in processed_text for word in ['como', 'quando', 'onde', 'por que', 'what', 'how', 'when', 'where', 'why', 'dúvida', 'questão'])
        has_action_request = any(word in processed_text for word in ['preciso', 'podem', 'aguardo', 'solicito', 'need', 'please', 'request'])
        is_greeting = any(word in processed_text for word in ['oi', 'olá', 'hi', 'hello'])
        
        high_priority_business = any(word in original_text_lower for word in [
            'reunião', 'reuniao', 'meeting', 'projeto', 'project', 'deadline', 'prazo',
            'urgente', 'urgent', 'problema', 'problem', 'relatório', 'relatorio', 'report',
            'apresentação', 'apresentacao', 'presentation', 'proposta', 'proposal',
            'cliente', 'client', 'contrato', 'contract', 'venda', 'sale'
        ])
        
        has_business_time = any(word in original_text_lower for word in [
            'amanhã', 'amanha', 'tomorrow', 'hoje', 'today', 'segunda', 'terça', 'quarta', 'quinta', 'sexta',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'horário', 'horario', 'time'
        ])
        
        if high_priority_business:
            return "Produtivo"
            
        if has_business_time and productive_score > 0:
            return "Produtivo"
        
        if productive_score >= 2 or has_question or has_action_request:
            return "Produtivo"
            
        if (unproductive_score >= 3 and not high_priority_business and 
            not has_business_time and productive_score == 0 and sentiment > 0.2):
            return "Improdutivo"
        
        if (unproductive_score > productive_score and is_greeting and 
            not has_action_request and not high_priority_business and not has_business_time):
            return "Improdutivo"
        
        return "Produtivo"
    
    def generate_response(self, text, classification):
        if classification == "Produtivo":
            responses = [
                "Recebi sua mensagem e entendo a importância do assunto. Vou priorizar este item e retornarei em breve.",
                "Obrigado por entrar em contato. Vou analisar sua questão e providenciar uma solução adequada.",
                "Mensagem recebida. Estou verificando as informações necessárias para fornecer uma resposta completa.",
                "Agradecemos o contato. Sua solicitação foi registrada e será tratada com a devida atenção.",
                "Entendi a necessidade. Vou mobilizar os recursos necessários para resolver esta questão."
            ]
        else:
            responses = [
                "Muito obrigado pela mensagem! Fico feliz em receber seu contato. Tenha um excelente dia!",
                "Que mensagem carinhosa! Agradeço muito pelas palavras gentis. Desejo tudo de bom para você!",
                "Obrigado por compartilhar esse momento especial conosco. Seus sentimentos são muito apreciados!",
                "Que bom receber uma mensagem tão positiva! Agradeço pela gentileza e retribuo os bons desejos.",
                "Muito obrigado! É sempre um prazer receber mensagens tão calorosas. Um grande abraço!"
            ]
        
        return random.choice(responses)

email_classifier = EmailClassifier()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_email():
    try:
        email_text = ""
        
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            
            if file.filename.lower().endswith('.txt'):
                email_text = file.read().decode('utf-8')
            elif file.filename.lower().endswith('.pdf'):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        email_text += page.extract_text()
                except Exception as e:
                    logger.error(f"Error reading PDF: {e}")
                    return jsonify({'error': 'Erro ao ler arquivo PDF'}), 400
            else:
                return jsonify({'error': 'Formato de arquivo não suportado. Use .txt ou .pdf'}), 400
        
        elif 'email_text' in request.form and request.form['email_text'].strip():
            email_text = request.form['email_text']
        
        else:
            return jsonify({'error': 'Por favor, forneça um texto ou arquivo para classificação'}), 400
        
        if not email_text.strip():
            return jsonify({'error': 'Conteúdo do email está vazio'}), 400
        
        classification = email_classifier.classify_email(email_text)
        response = email_classifier.generate_response(email_text, classification)
        
        if classification == "Produtivo":
            description = "Este email requer ação ou resposta específica"
        else:
            description = "Este email é informativo ou social, não requer ação específica"
        
        return jsonify({
            'classification': classification,
            'description': description,
            'response': response,
            'original_text': email_text[:500] + "..." if len(email_text) > 500 else email_text
        })
        
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        return jsonify({'error': f'Erro ao processar email: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'classifier_type': 'optimized_rule_based'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)