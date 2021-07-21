# moov
O Moov é um sistema de gerenciamento de transportes. Nele devem existir diversos tipos de usuários e permissões.

Por exemplo:
1. Admin (tem permissão para tudo)
2. Vendedor (tem permissão apenas para listar motoristas)
3. Financeiro (não tem permissão para nada relacionado aos motoristas)
O desafio consiste em criar uma API REST do sistema, com cadastro de usuários, empresas,
onde um usuário é vinculado a uma ou mais empresas e pode possuir diferentes permissões
em cada empresa.
Por exemplo:
1. O usuario1 pode ser vendedor na Empresa1 e na Empresa2 e financeiro na Empresa3,
dessa forma poderia listar os motoristas das Empresa1 e Empresa2, mas não poderia
listar os motoristas da Empresa3.
No desafio deve ser criado um endpoint também para cadastro de motoristas com "nome" e
"cnh" mais os dados que forem necessários para esse gerenciamento de permissões onde o
motorista é vinculado a uma empresa.
Quando um usuário cria um motorista, já deve ser vinculado qual empresa esse motorista
pertence (pegando essa informação do usuário que cadastrou o motorista via token de
autenticação ou algo assim, por questões de segurança)
Deve ser criado também um endpoint para listar os motoristas para testar as permissões.
Dados obrigatórios para o cadastro:
1. Empresa:
nome e cnpj
2. Usuário:
nome, email e senha
3. Motorista:
nome e cnh
Obs: Não precisa ser o CRUD completo, apenas as operações necessárias para o
funcionamento
