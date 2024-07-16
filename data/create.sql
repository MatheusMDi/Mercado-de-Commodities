-- Tabela CotacaoDolar
CREATE TABLE CotacaoDolar (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura DECIMAL(10, 2),
    Máxima DECIMAL(10, 2),
    Mínima DECIMAL(10, 2),
    Var VARCHAR(10)
);

-- Tabela CotacaoEuro
CREATE TABLE CotacaoEuro (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura DECIMAL(10, 2),
    Máxima DECIMAL(10, 2),
    Mínima DECIMAL(10, 2),
    Var VARCHAR(10)
);

-- Tabela CotacaoWon
CREATE TABLE CotacaoWon (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura DECIMAL(10, 2),
    Máxima DECIMAL(10, 2),
    Mínima DECIMAL(10, 2),
    Var VARCHAR(10)
);

-- Tabela CotacaoRinggit
CREATE TABLE CotacaoRinggit (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura DECIMAL(10, 2),
    Máxima DECIMAL(10, 2),
    Mínima DECIMAL(10, 2),
    Var VARCHAR(10)
);

-- Tabela CotacaoDirecional
CREATE TABLE CotacaoDirecional (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura DECIMAL(10, 2),
    Máxima DECIMAL(10, 2),
    Mínima DECIMAL(10, 2),
    Var VARCHAR(10)
);

-- Tabela CotacaoSteelRebar
CREATE TABLE CotacaoSteelRebar (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoSteelScrap
CREATE TABLE CotacaoSteelScrap (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoAluminum
CREATE TABLE CotacaoAluminum (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoIronOre
CREATE TABLE CotacaoIronOre (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoCopper
CREATE TABLE CotacaoCopper (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoSoybeanOil
CREATE TABLE CotacaoSoybeanOil (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoNaturalGas
CREATE TABLE CotacaoNaturalGas (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoBrentOil
CREATE TABLE CotacaoBrentOil (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoPPFutures
CREATE TABLE CotacaoPPFutures (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoPVCFutures
CREATE TABLE CotacaoPVCFutures (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);

-- Tabela CotacaoLLDPEFutures
CREATE TABLE CotacaoLLDPEFutures (
    data DATE NOT NULL,
    Simbolo VARCHAR(10),
    price DECIMAL(10, 2),
    Abertura VARCHAR(10),
    Máxima VARCHAR(10),
    Mínima VARCHAR(10),
    Var VARCHAR(10)
);
