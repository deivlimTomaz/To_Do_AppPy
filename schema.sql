CREATE TABLE IF NOT EXISTS tarefas (
	id INTEGER PRIMARY KEY,
	tipo TEXT NOT NULL CHECK (tipo IN
		('TarefaSimples', 'TarefaChecklist', 'TarefaRecorr')),
	titulo TEXT NOT NULL CHECK (length(trim(titulo)) > 0),
	descricao TEXT NOT NULL,
	prioridade TEXT NOT NULL CHECK (prioridade IN
		('BAIXA', 'MEDIA', 'ALTA')),
	data_vencimento TEXT NOT NULL,
	concluida INTEGER NOT NULL DEFAULT 0 CHECK (concluida IN (0,1))
);

CREATE TABLE IF NOT EXISTS itens_checklist (
	id INTEGER PRIMARY KEY,
	tarefa_id INTEGER NOT NULL,
	posicao INTEGER NOT NULL CHECK (posicao >= 0),
	texto TEXT NOT NULL CHECK (length(trim(texto)) > 0),
	feito INTEGER NOT NULL DEFAULT 0 CHECK (feito IN (0,1)),
	UNIQUE (tarefa_id, posicao),
	FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recorrencias (
	tarefa_id INTEGER PRIMARY KEY,
	frequencia TEXT NOT NULL CHECK (frequencia IN ('diaria', 'semanal', 'mensal', 'anual')),
	intervalo INTEGER NOT NULL CHECK (intervalo > 0),
	FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE
);
