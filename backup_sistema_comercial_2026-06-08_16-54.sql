--
-- PostgreSQL database dump
--

\restrict qYS5XYzCTb112RE1bGiiYKdfkQ7r1EwJzh1FRguJzNtgAGdTjdrchJoOBipqF5v

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: caixas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.caixas (
    id integer NOT NULL,
    data_abertura timestamp without time zone NOT NULL,
    data_fechamento timestamp without time zone,
    saldo_inicial numeric(12,2) NOT NULL,
    status character varying(20) NOT NULL,
    total_vendas_dinheiro numeric(12,2),
    total_vendas_pix numeric(12,2),
    total_vendas_cartao numeric(12,2),
    total_vendas_fiado numeric(12,2),
    usuario_id integer NOT NULL,
    diferenca_fechamento numeric(12,2),
    supervisor_id integer,
    valor_declarado_dinheiro numeric(12,2)
);


ALTER TABLE public.caixas OWNER TO postgres;

--
-- Name: caixas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.caixas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.caixas_id_seq OWNER TO postgres;

--
-- Name: caixas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.caixas_id_seq OWNED BY public.caixas.id;


--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    id integer NOT NULL,
    nome character varying(150) NOT NULL,
    cpf_cnpj character varying(18),
    telefone character varying(20),
    whatsapp character varying(20),
    email character varying(120),
    endereco character varying(255),
    criado_em timestamp without time zone
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: clientes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clientes_id_seq OWNER TO postgres;

--
-- Name: clientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clientes_id_seq OWNED BY public.clientes.id;


--
-- Name: itens_venda; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itens_venda (
    id integer NOT NULL,
    quantidade integer NOT NULL,
    preco_unitario numeric(10,2) NOT NULL,
    subtotal numeric(10,2) NOT NULL,
    venda_id integer NOT NULL,
    produto_id integer NOT NULL
);


ALTER TABLE public.itens_venda OWNER TO postgres;

--
-- Name: itens_venda_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.itens_venda_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.itens_venda_id_seq OWNER TO postgres;

--
-- Name: itens_venda_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.itens_venda_id_seq OWNED BY public.itens_venda.id;


--
-- Name: movimentacoes_estoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movimentacoes_estoque (
    id integer NOT NULL,
    tipo character varying(20) NOT NULL,
    quantidade integer NOT NULL,
    data_movimentacao timestamp without time zone,
    descricao character varying(255),
    produto_id integer NOT NULL,
    usuario_id integer NOT NULL
);


ALTER TABLE public.movimentacoes_estoque OWNER TO postgres;

--
-- Name: movimentacoes_estoque_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movimentacoes_estoque_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movimentacoes_estoque_id_seq OWNER TO postgres;

--
-- Name: movimentacoes_estoque_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movimentacoes_estoque_id_seq OWNED BY public.movimentacoes_estoque.id;


--
-- Name: produtos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produtos (
    id integer NOT NULL,
    codigo_interno character varying(50) NOT NULL,
    nome character varying(150) NOT NULL,
    descricao text,
    categoria character varying(50),
    preco_custo numeric(10,2) NOT NULL,
    preco_venda numeric(10,2) NOT NULL,
    quantidade_estoque integer NOT NULL,
    estoque_minimo integer NOT NULL,
    imagem_url character varying(255),
    criado_em timestamp without time zone
);


ALTER TABLE public.produtos OWNER TO postgres;

--
-- Name: produtos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produtos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produtos_id_seq OWNER TO postgres;

--
-- Name: produtos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produtos_id_seq OWNED BY public.produtos.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    nome_completo character varying(100) NOT NULL,
    password_hash character varying(256) NOT NULL,
    role character varying(20) NOT NULL,
    ativo boolean NOT NULL,
    precisa_alterar_senha boolean NOT NULL
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuarios_id_seq OWNER TO postgres;

--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: vendas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vendas (
    id integer NOT NULL,
    data_venda timestamp without time zone,
    total numeric(10,2) NOT NULL,
    forma_pagamento character varying(30) NOT NULL,
    status character varying(20) NOT NULL,
    cliente_id integer,
    usuario_id integer NOT NULL
);


ALTER TABLE public.vendas OWNER TO postgres;

--
-- Name: vendas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vendas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vendas_id_seq OWNER TO postgres;

--
-- Name: vendas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vendas_id_seq OWNED BY public.vendas.id;


--
-- Name: caixas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caixas ALTER COLUMN id SET DEFAULT nextval('public.caixas_id_seq'::regclass);


--
-- Name: clientes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id SET DEFAULT nextval('public.clientes_id_seq'::regclass);


--
-- Name: itens_venda id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_venda ALTER COLUMN id SET DEFAULT nextval('public.itens_venda_id_seq'::regclass);


--
-- Name: movimentacoes_estoque id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentacoes_estoque ALTER COLUMN id SET DEFAULT nextval('public.movimentacoes_estoque_id_seq'::regclass);


--
-- Name: produtos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos ALTER COLUMN id SET DEFAULT nextval('public.produtos_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Name: vendas id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vendas ALTER COLUMN id SET DEFAULT nextval('public.vendas_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
18af439f5bc8
\.


--
-- Data for Name: caixas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.caixas (id, data_abertura, data_fechamento, saldo_inicial, status, total_vendas_dinheiro, total_vendas_pix, total_vendas_cartao, total_vendas_fiado, usuario_id, diferenca_fechamento, supervisor_id, valor_declarado_dinheiro) FROM stdin;
16	2026-06-08 13:10:26.578478	2026-06-08 13:11:10.744825	100.00	Fechado	12.00	0.00	0.00	0.00	7	0.00	1	\N
28	2026-06-08 15:13:01.675951	2026-06-08 15:13:27.229728	100.00	Fechado	12.00	0.00	0.00	0.00	7	0.00	1	112.00
17	2026-06-08 13:18:11.944694	2026-06-08 13:20:31.212257	100.00	Fechado	72.00	12.00	12.00	0.00	7	24.00	1	\N
29	2026-06-08 15:26:41.978431	2026-06-08 15:27:14.401962	100.00	Fechado	12.00	0.00	0.00	0.00	7	0.00	1	112.00
3	2026-06-03 22:44:50.011315	2026-06-08 16:14:38.770597	1000.00	Fechado	0.00	0.00	0.00	0.00	5	-878.00	1	122.00
30	2026-06-08 16:15:47.510547	2026-06-08 19:31:59.788915	1000.00	Fechado	0.00	0.00	0.00	0.00	5	-900.00	1	100.00
18	2026-06-08 13:21:38.385354	2026-06-08 13:23:27.033722	100.00	Fechado	12.00	12.00	12.00	12.00	7	36.00	1	\N
31	2026-06-08 19:33:01.20293	\N	100.00	Aberto	12.00	0.00	0.00	0.00	5	0.00	1	0.00
19	2026-06-08 13:25:03.487447	2026-06-08 13:26:15.070148	100.00	Fechado	12.00	12.00	12.00	12.00	7	36.00	1	\N
20	2026-06-08 14:20:25.987924	\N	100.00	Aberto	0.00	0.00	0.00	0.00	1	0.00	\N	0.00
21	2026-06-08 14:20:45.404773	2026-06-08 14:21:49.587844	100.00	Fechado	12.00	12.00	12.00	12.00	7	0.00	1	112.00
22	2026-06-08 14:28:18.383192	2026-06-08 14:29:12.665803	100.00	Fechado	12.00	12.00	12.00	12.00	7	0.00	1	112.00
23	2026-06-08 14:29:57.819268	2026-06-08 14:30:20.175445	100.00	Fechado	12.00	0.00	0.00	0.00	7	-12.00	1	100.00
24	2026-06-08 14:35:23.36881	2026-06-08 14:35:40.04266	100.00	Fechado	12.00	0.00	0.00	0.00	7	-12.00	1	100.00
25	2026-06-08 14:37:59.999876	2026-06-08 14:38:48.557684	100.00	Fechado	12.00	12.00	12.00	12.00	7	0.00	1	112.00
4	2026-06-04 21:31:04.699226	2026-06-07 22:09:00.41952	100.00	Fechado	12.00	0.00	0.00	0.00	7	-12.00	1	\N
12	2026-06-07 22:21:28.290956	2026-06-07 22:21:49.812878	100.00	Fechado	12.00	0.00	0.00	0.00	7	-12.00	1	\N
1	2026-06-03 13:04:39.856934	2026-06-03 13:28:06.129244	100.00	Fechado	0.00	24.00	0.00	20.00	1	0.00	\N	\N
5	2026-06-06 20:35:17.172469	\N	100.00	Aberto	0.00	0.00	0.00	0.00	8	0.00	\N	\N
6	2026-06-06 21:10:28.506094	\N	100.00	Aberto	0.00	0.00	0.00	0.00	4	0.00	\N	\N
2	2026-06-03 13:41:24.042394	2026-06-06 22:35:08.065556	100.00	Fechado	186.00	0.00	0.00	0.00	1	0.00	\N	\N
7	2026-06-06 22:35:28.906564	2026-06-06 22:35:48.232321	100.00	Fechado	0.00	0.00	0.00	0.00	1	0.00	\N	\N
8	2026-06-06 22:38:44.738833	2026-06-06 22:38:55.591967	100.00	Fechado	0.00	0.00	0.00	0.00	1	0.00	\N	\N
9	2026-06-06 22:47:35.712891	2026-06-07 21:05:45.622883	100.00	Fechado	17.00	0.00	0.00	0.00	1	0.00	\N	\N
10	2026-06-07 21:25:03.048143	2026-06-07 21:55:23.128743	100.00	Fechado	327.00	0.00	0.00	0.00	1	0.00	\N	\N
11	2026-06-07 22:03:50.035088	2026-06-07 22:04:16.056796	1000.00	Fechado	12.00	0.00	0.00	0.00	1	0.00	\N	\N
13	2026-06-07 22:44:53.58311	2026-06-07 22:45:20.11917	100.00	Fechado	12.00	0.00	0.00	0.00	7	-12.00	1	\N
26	2026-06-08 14:41:45.699342	2026-06-08 14:42:24.380888	100.00	Fechado	12.00	12.00	12.00	12.00	7	0.00	1	112.00
14	2026-06-08 12:57:42.182365	2026-06-08 13:01:44.724969	100.00	Fechado	132.00	0.00	0.00	0.00	7	-132.00	1	\N
15	2026-06-08 13:02:26.777955	2026-06-08 13:03:08.304852	100.00	Fechado	0.00	0.00	0.00	0.00	7	12.00	1	\N
27	2026-06-08 15:07:28.666096	2026-06-08 15:08:22.413192	100.00	Fechado	12.00	12.00	12.00	12.00	7	0.00	1	112.00
\.


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes (id, nome, cpf_cnpj, telefone, whatsapp, email, endereco, criado_em) FROM stdin;
1	lucas almeida	88899977772	94958544455	69999999999	lucas@gamil.com	rua brasila	2026-06-02 00:43:45.382489
3	Alice	888.555.666-64	(11) 9999-9999	(11) 98855-5555	alice@gmail.com	rua Sao Paulo	2026-06-02 15:29:27.748514
\.


--
-- Data for Name: itens_venda; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.itens_venda (id, quantidade, preco_unitario, subtotal, venda_id, produto_id) FROM stdin;
1	4	5.00	20.00	1	3
2	2	12.00	24.00	2	2
3	3	12.00	36.00	3	2
4	1	5.00	5.00	4	3
5	4	12.00	48.00	5	2
6	1	5.00	5.00	6	3
7	1	12.00	12.00	7	2
8	1	5.00	5.00	8	3
9	1	12.00	12.00	9	2
10	1	12.00	12.00	10	2
11	1	5.00	5.00	11	3
12	1	12.00	12.00	12	2
13	1	5.00	5.00	13	3
14	1	12.00	12.00	14	2
15	1	5.00	5.00	15	3
16	1	12.00	12.00	16	2
17	1	5.00	5.00	17	3
18	1	12.00	12.00	18	2
19	1	5.00	5.00	19	3
20	1	12.00	12.00	20	2
21	1	5.00	5.00	21	3
22	1	12.00	12.00	22	2
23	1	5.00	5.00	23	3
24	1	12.00	12.00	24	2
25	1	5.00	5.00	25	3
26	1	12.00	12.00	26	2
27	39	5.00	195.00	27	3
28	1	12.00	12.00	28	2
29	100	12.00	1200.00	29	2
30	10	12.00	120.00	30	2
31	1	12.00	12.00	31	2
32	1	12.00	12.00	32	2
33	1	12.00	12.00	33	2
34	1	12.00	12.00	34	2
35	10	12.00	120.00	35	2
36	1	12.00	12.00	36	2
37	1	12.00	12.00	37	2
38	1	12.00	12.00	38	2
39	5	12.00	60.00	39	2
40	1	12.00	12.00	40	2
41	1	12.00	12.00	41	2
42	1	12.00	12.00	42	2
43	1	12.00	12.00	43	2
44	1	12.00	12.00	44	2
45	1	12.00	12.00	45	2
46	1	12.00	12.00	46	2
47	1	12.00	12.00	47	2
48	1	12.00	12.00	48	2
49	1	12.00	12.00	49	2
50	1	12.00	12.00	50	2
51	1	12.00	12.00	51	2
52	1	12.00	12.00	52	2
53	1	12.00	12.00	53	2
54	1	12.00	12.00	54	2
55	1	12.00	12.00	55	2
56	1	12.00	12.00	56	2
57	1	12.00	12.00	57	2
58	1	12.00	12.00	58	2
59	1	12.00	12.00	59	2
60	1	12.00	12.00	60	2
61	1	12.00	12.00	61	2
62	1	12.00	12.00	62	2
63	1	12.00	12.00	63	2
64	1	12.00	12.00	64	2
65	1	12.00	12.00	65	2
66	1	12.00	12.00	66	2
67	1	12.00	12.00	67	2
68	1	12.00	12.00	68	2
69	1	12.00	12.00	69	2
70	1	12.00	12.00	70	2
71	1	12.00	12.00	71	2
72	1	12.00	12.00	72	2
73	1	12.00	12.00	73	2
74	1	12.00	12.00	74	2
75	1	12.00	12.00	75	2
\.


--
-- Data for Name: movimentacoes_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movimentacoes_estoque (id, tipo, quantidade, data_movimentacao, descricao, produto_id, usuario_id) FROM stdin;
1	Saída	4	2026-06-03 13:05:48.715537	Venda realizada no PDV	3	1
2	Saída	2	2026-06-03 13:26:16.746316	Venda realizada no PDV	2	1
3	Saída	3	2026-06-03 13:41:45.817919	Venda realizada no PDV	2	1
4	Saída	1	2026-06-03 13:42:40.139371	Venda realizada no PDV	3	1
5	Saída	4	2026-06-03 13:48:23.331132	Venda realizada no PDV	2	1
6	Saída	1	2026-06-03 14:12:44.543472	Venda realizada no PDV	3	1
7	Saída	1	2026-06-03 14:16:31.499898	Venda realizada no PDV	2	1
8	Saída	1	2026-06-03 15:23:43.227745	Venda realizada no PDV	3	1
9	Saída	1	2026-06-03 15:46:12.950271	Venda realizada no PDV	2	1
10	Saída	1	2026-06-03 15:52:34.030088	Venda realizada no PDV	2	1
11	Saída	1	2026-06-03 15:54:01.782748	Venda realizada no PDV	3	1
12	Saída	1	2026-06-03 16:16:17.076223	Venda realizada no PDV	2	1
13	Saída	1	2026-06-03 16:17:02.739559	Venda realizada no PDV	3	1
14	Saída	1	2026-06-03 16:18:06.739924	Venda realizada no PDV	2	1
15	Saída	1	2026-06-03 19:25:01.982956	Venda realizada no PDV	3	1
16	Saída	1	2026-06-03 19:53:54.459986	Venda realizada no PDV	2	1
17	Entrada	1	2026-06-03 19:55:07.744144	Estorno/Cancelamento da Venda ID 16	2	1
18	Saída	1	2026-06-03 20:02:25.359779	Venda realizada no PDV	3	1
19	Entrada	1	2026-06-03 20:02:30.095028	Estorno/Cancelamento da Venda ID 17	3	1
20	Saída	1	2026-06-03 20:06:36.973677	Venda realizada no PDV	2	1
21	Entrada	1	2026-06-03 20:06:41.671326	Estorno/Cancelamento da Venda ID 18	2	1
22	Saída	1	2026-06-03 20:08:15.397479	Venda realizada no PDV	3	1
23	Entrada	1	2026-06-03 20:08:24.164884	Estorno/Cancelamento da Venda ID 19	3	1
24	Saída	1	2026-06-03 20:08:49.69535	Venda realizada no PDV	2	1
25	Entrada	1	2026-06-03 20:08:54.020145	Estorno/Cancelamento da Venda ID 20	2	1
26	Saída	1	2026-06-04 21:37:54.035381	Venda realizada no PDV	3	1
27	Entrada	1	2026-06-04 21:38:00.786562	Estorno/Cancelamento da Venda ID 21	3	1
28	Saída	1	2026-06-04 22:31:44.743614	Venda realizada no PDV	2	1
29	Entrada	1	2026-06-04 22:31:48.133779	Estorno/Cancelamento da Venda ID 22	2	1
30	Saída	1	2026-06-04 22:35:40.822629	Venda realizada no PDV	3	7
31	Entrada	1	2026-06-04 22:35:49.160567	Estorno/Cancelamento da Venda ID 23	3	7
32	Saída	1	2026-06-06 20:22:33.690911	Venda realizada no PDV	2	1
33	Saída	1	2026-06-06 22:47:44.766192	Venda realizada no PDV	3	1
34	Saída	1	2026-06-06 22:58:16.645611	Venda realizada no PDV	2	1
35	Saída	39	2026-06-07 21:41:15.660853	Venda realizada no PDV	3	1
36	Saída	1	2026-06-07 21:41:40.934672	Venda realizada no PDV	2	1
37	Saída	100	2026-06-07 21:41:54.368097	Venda realizada no PDV	2	1
38	Entrada	100	2026-06-07 21:42:11.984911	Estorno/Cancelamento da Venda ID 29	2	1
39	Saída	10	2026-06-07 21:54:45.715786	Venda realizada no PDV	2	1
40	Saída	1	2026-06-07 22:03:58.196775	Venda realizada no PDV	2	1
41	Saída	1	2026-06-07 22:08:43.091035	Venda realizada no PDV	2	7
42	Saída	1	2026-06-07 22:21:33.967424	Venda realizada no PDV	2	7
43	Saída	1	2026-06-07 22:45:02.538183	Venda realizada no PDV	2	7
44	Saída	10	2026-06-08 12:58:37.974282	Venda realizada no PDV	2	7
45	Saída	1	2026-06-08 12:59:37.148908	Venda realizada no PDV	2	7
46	Saída	1	2026-06-08 13:10:41.263665	Venda realizada no PDV	2	7
47	Saída	1	2026-06-08 13:18:20.725737	Venda realizada no PDV	2	7
48	Saída	5	2026-06-08 13:18:53.843178	Venda realizada no PDV	2	7
49	Saída	1	2026-06-08 13:19:08.764578	Venda realizada no PDV	2	7
50	Saída	1	2026-06-08 13:19:32.868794	Venda realizada no PDV	2	7
51	Saída	1	2026-06-08 13:21:47.608747	Venda realizada no PDV	2	7
52	Saída	1	2026-06-08 13:21:59.065308	Venda realizada no PDV	2	7
53	Saída	1	2026-06-08 13:22:19.842333	Venda realizada no PDV	2	7
54	Saída	1	2026-06-08 13:22:38.122006	Venda realizada no PDV	2	7
55	Entrada	1	2026-06-08 13:22:51.390267	Estorno/Cancelamento da Venda ID 45	2	7
56	Saída	1	2026-06-08 13:23:06.92059	Venda realizada no PDV	2	7
57	Saída	1	2026-06-08 13:25:13.050422	Venda realizada no PDV	2	7
58	Saída	1	2026-06-08 13:25:28.69702	Venda realizada no PDV	2	7
59	Saída	1	2026-06-08 13:25:42.72487	Venda realizada no PDV	2	7
60	Saída	1	2026-06-08 13:25:50.58533	Venda realizada no PDV	2	7
61	Saída	1	2026-06-08 14:20:56.374564	Venda realizada no PDV	2	7
62	Saída	1	2026-06-08 14:21:09.018723	Venda realizada no PDV	2	7
63	Saída	1	2026-06-08 14:21:17.500224	Venda realizada no PDV	2	7
64	Saída	1	2026-06-08 14:21:27.765389	Venda realizada no PDV	2	7
65	Saída	1	2026-06-08 14:28:30.344013	Venda realizada no PDV	2	7
66	Saída	1	2026-06-08 14:28:38.662965	Venda realizada no PDV	2	7
67	Saída	1	2026-06-08 14:28:45.837131	Venda realizada no PDV	2	7
68	Saída	1	2026-06-08 14:28:55.16196	Venda realizada no PDV	2	7
69	Saída	1	2026-06-08 14:30:06.153537	Venda realizada no PDV	2	7
70	Saída	1	2026-06-08 14:35:27.786883	Venda realizada no PDV	2	7
71	Saída	1	2026-06-08 14:38:09.18065	Venda realizada no PDV	2	7
72	Saída	1	2026-06-08 14:38:17.184562	Venda realizada no PDV	2	7
73	Saída	1	2026-06-08 14:38:24.020216	Venda realizada no PDV	2	7
74	Saída	1	2026-06-08 14:38:29.84771	Venda realizada no PDV	2	7
75	Saída	1	2026-06-08 14:41:52.298135	Venda realizada no PDV	2	7
76	Saída	1	2026-06-08 14:41:58.020623	Venda realizada no PDV	2	7
77	Saída	1	2026-06-08 14:42:04.390861	Venda realizada no PDV	2	7
78	Saída	1	2026-06-08 14:42:12.17847	Venda realizada no PDV	2	7
79	Saída	1	2026-06-08 15:07:46.560166	Venda realizada no PDV	2	7
80	Saída	1	2026-06-08 15:07:52.899659	Venda realizada no PDV	2	7
81	Saída	1	2026-06-08 15:07:59.225598	Venda realizada no PDV	2	7
82	Saída	1	2026-06-08 15:08:04.977647	Venda realizada no PDV	2	7
83	Saída	1	2026-06-08 15:13:07.420067	Venda realizada no PDV	2	7
84	Saída	1	2026-06-08 15:26:59.494063	Venda realizada no PDV	2	7
85	Saída	1	2026-06-08 19:33:14.481124	Venda realizada no PDV	2	5
\.


--
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produtos (id, codigo_interno, nome, descricao, categoria, preco_custo, preco_venda, quantidade_estoque, estoque_minimo, imagem_url, criado_em) FROM stdin;
3	PRD00003	coca-cola lata 200ml	Refrig	Bebidas	3.00	5.00	0	5	uploads/produtos/PRD00003_coca-cola-lata200ml.jpg	2026-06-02 15:27:24.205688
2	PRD00002	coca-cola 2l	Refrig	Bebidas	7.00	12.00	116	5	uploads/produtos/PRD00002_coca-cola2l.jpg	2026-06-01 23:46:57.433905
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (id, username, nome_completo, password_hash, role, ativo, precisa_alterar_senha) FROM stdin;
1	admin123	sivaldo	scrypt:32768:8:1$YJ6SpCyCoqtMwDIN$f659b9159e8986cbad82e6e86d1616ce69add1ae366d9df2018cf7087f0a2cb1e88d64b5ff8708914bcd627e7043f6c8817944b930aee2a73ae0ff1f06348fa7	administrador	t	f
5	maria	maria	scrypt:32768:8:1$Bsrm5YhIJAbhhDZs$e25b9bda9c12b5c656011c9ac84c62d8e156dfaa0763e8f5b75ce97b9391e521fc4b9c220d75da0724c46eac96ec665777c95703ffa1fcb2e2d4b73a0e1e34e5	operador	t	f
2	alice	Alice Moraes Baia	scrypt:32768:8:1$KizjpSgrN2bRaQC1$d4bade9fb4b29aad6b9f8aee554e17d80e6e4e23ecd1f876334d4720d981eb8dde29361a2887093b0d902cda80bb3ddc62878f73f5270bac1d450b54707d1985	administrador	t	f
7	mara	mara	scrypt:32768:8:1$WOfRJbago6PxXvi7$eb83897040c16c8a90b3f038ddb0e5aabcd109a6483d5626226183e75f18e23c1dc6c116ccbf2ac3b2cfde693f28d17bc09b0e9f71e6e2767f19812a14f7d2f2	operador	t	f
8	mike	mike	scrypt:32768:8:1$xPTpHP78VBtUrCTX$5f7340536fcf6f478d0fc1b61e5e591ae8e5de7f8021f100736c19cb8e9b091f6d263d1f1e37fb09348e0d400eb45960f4fdd12380566ebd4ce67b82cf6f9f21	operador	t	f
4	billy	Billy de Kid	scrypt:32768:8:1$MaNodg6MI6uMOeXZ$0046cd3b39f1b973805e33d7d09672177e3414ba7dc9f6c48cf257eee1438cc4f3a9452638c28a9b231f1bc874c3e9c88391abd70762ce4670edf758980fb5cc	operador	t	f
\.


--
-- Data for Name: vendas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vendas (id, data_venda, total, forma_pagamento, status, cliente_id, usuario_id) FROM stdin;
1	2026-06-03 13:05:48.703873	20.00	Fiado	Concluída	3	1
2	2026-06-03 13:26:16.743551	24.00	PIX	Concluída	\N	1
3	2026-06-03 13:41:45.815411	36.00	Dinheiro	Concluída	\N	1
4	2026-06-03 13:42:40.136614	5.00	Dinheiro	Concluída	\N	1
5	2026-06-03 13:48:23.329318	48.00	Dinheiro	Concluída	\N	1
6	2026-06-03 14:12:44.539467	5.00	Dinheiro	Concluída	\N	1
7	2026-06-03 14:16:31.49777	12.00	Dinheiro	Concluída	\N	1
8	2026-06-03 15:23:43.213109	5.00	Dinheiro	Concluída	\N	1
9	2026-06-03 15:46:12.948122	12.00	Dinheiro	Concluída	\N	1
10	2026-06-03 15:52:34.018865	12.00	Dinheiro	Concluída	\N	1
11	2026-06-03 15:54:01.780387	5.00	Dinheiro	Concluída	\N	1
12	2026-06-03 16:16:17.072134	12.00	Dinheiro	Concluída	\N	1
13	2026-06-03 16:17:02.733795	5.00	Dinheiro	Concluída	\N	1
14	2026-06-03 16:18:06.738358	12.00	Dinheiro	Concluída	\N	1
15	2026-06-03 19:25:01.981086	5.00	Dinheiro	Concluída	\N	1
16	2026-06-03 19:53:54.449932	12.00	Dinheiro	Cancelada	\N	1
17	2026-06-03 20:02:25.357709	5.00	Dinheiro	Cancelada	\N	1
18	2026-06-03 20:06:36.971071	12.00	Dinheiro	Cancelada	\N	1
19	2026-06-03 20:08:15.395628	5.00	Dinheiro	Cancelada	\N	1
20	2026-06-03 20:08:49.690694	12.00	Dinheiro	Cancelada	\N	1
21	2026-06-04 21:37:54.025896	5.00	Dinheiro	Cancelada	\N	1
22	2026-06-04 22:31:44.734466	12.00	Dinheiro	Cancelada	\N	1
23	2026-06-04 22:35:40.816613	5.00	Dinheiro	Cancelada	\N	7
24	2026-06-06 20:22:33.680702	12.00	Dinheiro	Concluída	\N	1
25	2026-06-06 22:47:44.758848	5.00	Dinheiro	Concluída	\N	1
26	2026-06-06 22:58:16.639159	12.00	Dinheiro	Concluída	\N	1
27	2026-06-07 21:41:15.654725	195.00	Dinheiro	Concluída	\N	1
28	2026-06-07 21:41:40.932806	12.00	Dinheiro	Concluída	\N	1
29	2026-06-07 21:41:54.365462	1200.00	Dinheiro	Cancelada	\N	1
30	2026-06-07 21:54:45.714252	120.00	Dinheiro	Concluída	\N	1
31	2026-06-07 22:03:58.191251	12.00	Dinheiro	Concluída	\N	1
32	2026-06-07 22:08:43.086492	12.00	Dinheiro	Concluída	\N	7
33	2026-06-07 22:21:33.962132	12.00	Dinheiro	Concluída	\N	7
34	2026-06-07 22:45:02.530482	12.00	Dinheiro	Concluída	\N	7
35	2026-06-08 12:58:37.967815	120.00	Dinheiro	Concluída	\N	7
36	2026-06-08 12:59:37.146665	12.00	Dinheiro	Concluída	3	7
37	2026-06-08 13:10:41.25747	12.00	Dinheiro	Concluída	\N	7
38	2026-06-08 13:18:20.723148	12.00	Dinheiro	Concluída	\N	7
39	2026-06-08 13:18:53.84146	60.00	Dinheiro	Concluída	\N	7
40	2026-06-08 13:19:08.763099	12.00	PIX	Concluída	\N	7
41	2026-06-08 13:19:32.866208	12.00	Cartão	Concluída	\N	7
42	2026-06-08 13:21:47.606841	12.00	Dinheiro	Concluída	\N	7
43	2026-06-08 13:21:59.063922	12.00	PIX	Concluída	\N	7
44	2026-06-08 13:22:19.841044	12.00	Cartão	Concluída	\N	7
45	2026-06-08 13:22:38.120439	12.00	Fiado	Cancelada	\N	7
46	2026-06-08 13:23:06.918163	12.00	Fiado	Concluída	1	7
47	2026-06-08 13:25:13.049145	12.00	Dinheiro	Concluída	\N	7
48	2026-06-08 13:25:28.695127	12.00	PIX	Concluída	\N	7
49	2026-06-08 13:25:42.723464	12.00	Cartão	Concluída	\N	7
50	2026-06-08 13:25:50.584062	12.00	Fiado	Concluída	\N	7
51	2026-06-08 14:20:56.365313	12.00	Dinheiro	Concluída	\N	7
52	2026-06-08 14:21:09.017027	12.00	PIX	Concluída	\N	7
53	2026-06-08 14:21:17.497217	12.00	Cartão	Concluída	\N	7
54	2026-06-08 14:21:27.763061	12.00	Fiado	Concluída	\N	7
55	2026-06-08 14:28:30.338996	12.00	Dinheiro	Concluída	\N	7
56	2026-06-08 14:28:38.660692	12.00	PIX	Concluída	\N	7
57	2026-06-08 14:28:45.835633	12.00	Cartão	Concluída	\N	7
58	2026-06-08 14:28:55.160523	12.00	Fiado	Concluída	\N	7
59	2026-06-08 14:30:06.15195	12.00	Dinheiro	Concluída	\N	7
60	2026-06-08 14:35:27.784573	12.00	Dinheiro	Concluída	\N	7
61	2026-06-08 14:38:09.179393	12.00	Dinheiro	Concluída	\N	7
62	2026-06-08 14:38:17.182815	12.00	PIX	Concluída	\N	7
63	2026-06-08 14:38:24.018044	12.00	Cartão	Concluída	\N	7
64	2026-06-08 14:38:29.845029	12.00	Fiado	Concluída	\N	7
65	2026-06-08 14:41:52.296901	12.00	Dinheiro	Concluída	\N	7
66	2026-06-08 14:41:58.018537	12.00	PIX	Concluída	\N	7
67	2026-06-08 14:42:04.389459	12.00	Cartão	Concluída	\N	7
68	2026-06-08 14:42:12.176932	12.00	Fiado	Concluída	\N	7
69	2026-06-08 15:07:46.556753	12.00	Dinheiro	Concluída	\N	7
70	2026-06-08 15:07:52.898019	12.00	Cartão	Concluída	\N	7
71	2026-06-08 15:07:59.222374	12.00	PIX	Concluída	\N	7
72	2026-06-08 15:08:04.975956	12.00	Fiado	Concluída	\N	7
73	2026-06-08 15:13:07.415678	12.00	Dinheiro	Concluída	\N	7
74	2026-06-08 15:26:59.489454	12.00	Dinheiro	Concluída	\N	7
75	2026-06-08 19:33:14.475946	12.00	Dinheiro	Concluída	\N	5
\.


--
-- Name: caixas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.caixas_id_seq', 31, true);


--
-- Name: clientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clientes_id_seq', 3, true);


--
-- Name: itens_venda_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.itens_venda_id_seq', 75, true);


--
-- Name: movimentacoes_estoque_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movimentacoes_estoque_id_seq', 85, true);


--
-- Name: produtos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produtos_id_seq', 3, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 8, true);


--
-- Name: vendas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vendas_id_seq', 75, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: caixas caixas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caixas
    ADD CONSTRAINT caixas_pkey PRIMARY KEY (id);


--
-- Name: clientes clientes_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_email_key UNIQUE (email);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id);


--
-- Name: itens_venda itens_venda_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_venda
    ADD CONSTRAINT itens_venda_pkey PRIMARY KEY (id);


--
-- Name: movimentacoes_estoque movimentacoes_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentacoes_estoque
    ADD CONSTRAINT movimentacoes_estoque_pkey PRIMARY KEY (id);


--
-- Name: produtos produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: vendas vendas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vendas
    ADD CONSTRAINT vendas_pkey PRIMARY KEY (id);


--
-- Name: ix_clientes_cpf_cnpj; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_clientes_cpf_cnpj ON public.clientes USING btree (cpf_cnpj);


--
-- Name: ix_clientes_nome; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_clientes_nome ON public.clientes USING btree (nome);


--
-- Name: ix_movimentacoes_estoque_data_movimentacao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_movimentacoes_estoque_data_movimentacao ON public.movimentacoes_estoque USING btree (data_movimentacao);


--
-- Name: ix_produtos_categoria; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_produtos_categoria ON public.produtos USING btree (categoria);


--
-- Name: ix_produtos_codigo_interno; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_produtos_codigo_interno ON public.produtos USING btree (codigo_interno);


--
-- Name: ix_produtos_nome; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_produtos_nome ON public.produtos USING btree (nome);


--
-- Name: ix_usuarios_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_usuarios_username ON public.usuarios USING btree (username);


--
-- Name: ix_vendas_data_venda; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_vendas_data_venda ON public.vendas USING btree (data_venda);


--
-- Name: caixas caixas_supervisor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caixas
    ADD CONSTRAINT caixas_supervisor_id_fkey FOREIGN KEY (supervisor_id) REFERENCES public.usuarios(id);


--
-- Name: caixas caixas_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caixas
    ADD CONSTRAINT caixas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: itens_venda itens_venda_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_venda
    ADD CONSTRAINT itens_venda_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id);


--
-- Name: itens_venda itens_venda_venda_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_venda
    ADD CONSTRAINT itens_venda_venda_id_fkey FOREIGN KEY (venda_id) REFERENCES public.vendas(id);


--
-- Name: movimentacoes_estoque movimentacoes_estoque_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentacoes_estoque
    ADD CONSTRAINT movimentacoes_estoque_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id);


--
-- Name: movimentacoes_estoque movimentacoes_estoque_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentacoes_estoque
    ADD CONSTRAINT movimentacoes_estoque_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: vendas vendas_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vendas
    ADD CONSTRAINT vendas_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.clientes(id);


--
-- Name: vendas vendas_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vendas
    ADD CONSTRAINT vendas_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- PostgreSQL database dump complete
--

\unrestrict qYS5XYzCTb112RE1bGiiYKdfkQ7r1EwJzh1FRguJzNtgAGdTjdrchJoOBipqF5v

