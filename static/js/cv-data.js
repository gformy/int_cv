const CV_ITEMS = [
  { cat:'🎓', cat_name:'Istruzione', title:'Perito Tecnico Informatico', text:'Diploma con focus su informatica, linguaggi programmati: Assembly, C/C++, Java, HTML/CSS, PhP, DML/DDL,SQL.', color:'#ffd700', glow:'rgba(255,215,0,0.6)' },
  { cat:'🎓', cat_name:'Istruzione', title:'Laurea in Informatica', text:'Percorso universitario con specializzazione in algoritmi, reti, sistemi operativi, sicurezza informatica, Base dati.', color:'#ffd700', glow:'rgba(255,215,0,0.6)' },
  { cat:'🎓', cat_name:'Istruzione', title:'Tesi Innovativa', text:'Progetto di sviluppo di una rete neurale collegata a MongoDB.', color:'#ffd700', glow:'rgba(255,215,0,0.6)' },

  { cat:'🔧', cat_name:'Tirocinio', title:'Montaggio Schede Domotiche', text:'Installazione e configurazione di centraline e moduli domotici.', color:'#ff6b35', glow:'rgba(255,107,53,0.6)' },
  { cat:'🔧', cat_name:'Tirocinio', title:'Costruttore di Base Dati', text:'Studio di fattibilità e Implementazione di un Data Base dnato al Museo della Shoah', color:'#ff6b35', glow:'rgba(255,107,53,0.6)' },

  { cat:'⚡', cat_name:'Volontariato', title:'Volontario UEFA', text:'Supporto organizzativo per partite internazionali: accreditamenti e gestione tifosi.', color:'#4ecdc4', glow:'rgba(78,205,196,0.6)' },
  { cat:'⚡', cat_name:'Volontariato', title:'Formula E (E-Prix)', text:'Volontario alla Formula Elettrica: logistica pit-lane e assistenza pubblico.', color:'#4ecdc4', glow:'rgba(78,205,196,0.6)' },
  { cat:'⚡', cat_name:'Volontariato', title:'Gestione Alta Pressione', text:'Capacità di lavorare in eventi con migliaia di persone mantenendo la calma.', color:'#4ecdc4', glow:'rgba(78,205,196,0.6)' },

  { cat:'💻', cat_name:'Sviluppatore', title:'Python & Java Backend', text:'Sviluppo di API REST robuste, microservizi e sistemi distribuiti.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'React & Vue Frontend', text:'Interfacce responsive e moderne con focus su UX e performance.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'Docker & DevOps', text:'Containerizzazione, CI/CD pipelines e deploy automatizzato.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'SQL & NoSQL Database', text:'Progettazione di schemi, query ottimizzate, Oracle, PostgreSQL e MongoDB.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'Metodologie Agile', text:'Scrum, sprint planning, code review e continuous integration.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },
  { cat:'💻', cat_name:'Sviluppatore', title:'Git & Versionamento', text:'Workflow professionale con branch, PR e gestione repository.', color:'#a855f7', glow:'rgba(168,85,247,0.6)' },

  { cat:'🏥', cat_name:'ASL', title:'BDA', text:'Sviluppo e Gestione dei Database sia per il personale interno che per i Cittadini.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'Azienda Sanitaria Locale', text:'Sviluppatore software per sistemi sanitari critici e cartelle cliniche.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'Standard HL7/FHIR', text:'Integrazione di sistemi per l\'interoperabilità dei dati sanitari.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'Sistema CUP', text:'Gestione prenotazioni e accessi ai servizi sanitari per i cittadini.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },
  { cat:'🏥', cat_name:'ASL', title:'GDPR & Privacy', text:'Rispetto normative sulla privacy in contesti regolamentati e critici.', color:'#f43f5e', glow:'rgba(244,63,94,0.6)' },

  { cat:'🌟', cat_name:'Soft Skills', title:'Problem Solving Creativo', text:'Approccio analitico e laterale ai problemi tecnici e organizzativi.', color:'#06b6d4', glow:'rgba(6,182,212,0.6)' },
  { cat:'🌟', cat_name:'Soft Skills', title:'Team Working', text:'Esperienza in team multidisciplinari in contesti sia tecnici che di evento.', color:'#06b6d4', glow:'rgba(6,182,212,0.6)' },
  { cat:'🌟', cat_name:'Soft Skills', title:'Adattabilità', text:'Passato dall\'elettronica al codice, dalla sanità allo sport. Versatile!', color:'#06b6d4', glow:'rgba(6,182,212,0.6)' },
];

const SKILL_MAP = {
  Sviluppatore: ['python', 'react', 'java', 'sql', 'docker'],
  Tirocinio: ['knx'],
  Istruzione: ['python', 'java'],
  ASL: ['sql', 'python'],
};