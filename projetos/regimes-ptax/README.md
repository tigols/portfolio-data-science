## Projeto: Regimes de volatilidade da PTAX com Markov Switching

### Pergunta
O câmbio real-dólar alterna entre períodos calmos e períodos de estresse? É possível identificar esses regimes e, mais importante, detectá-los em tempo real, sem olhar o futuro?

### Dados
- PTAX venda (série 1 do SGS/BCB), diária, de 01/01/2016 a 31/12/2025, obtida pela API do Banco Central com o pipeline de `src/bcb.py`.
- Variável modelada: retorno percentual diário, ( $r_t = 100 \cdot (P_t / P_{t-1} - 1) $). O preço tem tendência (de ~R$ 3 para ~R$ 6); o retorno não, e é nele que a volatilidade aparece.

### Modelo
Regressão com troca de regimes de Markov (`statsmodels.tsa.MarkovRegression`), com 2 regimes, média e variância próprias em cada regime:

$$ r_t \sim N(\mu_{S_t}, \sigma^2_{S_t}), \qquad P(S_t = j \mid S_{t-1} = i) = p_{ij} $$

O regime \(S_t\) não é observado: o modelo estima a probabilidade de cada dia estar em cada regime.

Antes da PTAX, validei o modelo com dados simulados (blocos com variâncias conhecidas), para entender a leitura do `summary()` e os limites do método. Com blocos muito parecidos entre si, o modelo não consegue separá-los.

### Resultados com a série completa (in-sample)
| | Regime calmo | Regime de estresse |
|---|---|---|
| Variância (\(\sigma^2\)) | 0,41 | 1,63 |
| Desvio diário | ~0,64% | ~1,28% |
| Probabilidade de permanecer | 0,985 | 0,967 |
| Duração média | ~67 dias úteis | ~31 dias úteis |

- As médias não são significativas nos dois regimes: o regime é definido pela **volatilidade**, não pela direção do dólar. Preço subindo ou caindo com força cai no mesmo regime.
- Os períodos de estresse coincidem com eventos conhecidos (associação, não causalidade):
  - **2016:** processo de impeachment da presidente Dilma. O dólar caía, porque o mercado apostava na troca de governo, mas a volatilidade era alta.
  - **2018:** greve dos caminhoneiros (maio) e eleições presidenciais, com a incerteza sobre política fiscal levando à saída de capital estrangeiro.
  - **2020:** pandemia de COVID-19, com estresse durante praticamente todo o ano.

### Walk-forward: o modelo funciona sem ver o futuro?
A análise acima tem vazamento de dados por dois motivos:
1. A **probabilidade suavizada** usa a série inteira: $(P(S_t \mid y_1, \dots, y_T))$. A **filtrada** usa só o passado: $(P(S_t \mid y_1, \dots, y_t))$.
2. Os **parâmetros** foram estimados com os 10 anos, inclusive com os dias que estamos classificando.

**Corte único (treino até 2019, teste em 2020):** o modelo treinado só com dados até 2019 aprendeu um estresse diferente, com variância de 3,90 e duração média de **~4 dias** (choques curtos, como o de maio de 2017). Aplicado a 2020 com parâmetros fixos, ele detecta o início da crise em março, mas **não sustenta** o regime: entra e sai do estresse o ano inteiro.

**Walk-forward mensal (janela expansiva):** a cada mês, o modelo é reajustado só com os dados anteriores e aplicado (filtro, sem reestimar) aos dias do mês. Resultado de 2020 a 2025:
- Em 2020, o estresse é sustentado por mais tempo que no corte único, porque, mês a mês, o modelo aprende que estresses longos existem.
- Estresse no fim de 2022 (eleições), um período majoritariamente calmo entre 2023 e 2024, e nova alta de volatilidade no início de 2025, que pode estar relacionada às tensões diplomáticas com os EUA, ao julgamento de Jair Bolsonaro e às tarifas americanas.

### Calibração: quando o modelo diz 70%, acontece 70%?
Como o regime não é observável, defini um alvo: $(y_t = 1)$ se o desvio padrão dos retornos dos **5 dias seguintes** passar de um limite. O limite é calculado **só com dados até 2019**. A comparação é feita pelo Brier score, ($ \frac{1}{n}\sum (p_t - y_t)^2 $), contra um chute que sempre prevê a taxa-base.

| Limite | Valor | Brier do modelo | Brier do chute |
|---|---|---|---|
| Média | 0,741 | 0,294 | 0,247 |
| P75 | 0,895 | 0,218 | 0,211 |
| P80 | 0,961 | **0,190** | 0,192 |
| P90 | 1,201 | 0,156 | 0,130 |
| P95 | 1,427 | 0,128 | 0,076 |
| Ancorado no modelo | 1,078 | 0,170 | 0,163 |

O limite ancorado no modelo é o ponto em que um dia fica igualmente provável nos dois regimes, onde as duas normais se cruzam:

$$ |r|^* = \sqrt{\frac{2\ln(s_1/s_0)\, s_0^2 s_1^2}{s_1^2 - s_0^2}} $$

**Leitura:**
- Com limite baixo (média), o modelo é **subconfiante**: o alvo marca dias demais.
- Com limite alto (P90, P95), ele é **superconfiante**: quando diz ~92%, só ~33% dos dias são estresse com o P95.
- Só o P80 empata com o chute. O limite ancorado (1,08), que fica entre a média e o P95, não chega a bater o chute.
- **Conclusão:** o modelo é bom para **detectar mudanças de volatilidade**, mas suas probabilidades não estão calibradas para serem usadas diretamente como probabilidade de estresse.

### Limitações
- **Instabilidade de parâmetros:** o que o modelo entende por "estresse" muda com os dados (~4 dias com treino até 2019, contra ~31 dias com a série completa).
- **Vazamento** nas probabilidades suavizadas, o que o walk-forward mostra e corrige.
- **Dois regimes** são uma simplificação. Com 3 regimes, o modelo não convergiu de forma estável nos testes com dados simulados.
- **Escolha do alvo:** a calibração depende do limite escolhido, por isso mostro a sensibilidade em vez de um número só.
- **Observações sobrepostas:** as janelas de 5 dias se sobrepõem, então os dias não são independentes, e diferenças pequenas de Brier podem ser ruído.
- A associação com eventos políticos e econômicos é **hipótese**, não causa.

### Próximos passos
- Recalibrar as probabilidades (isotônica ou Platt) no próprio walk-forward.
- Testar a probabilidade prevista (`predicted_marginal_probabilities`, que usa só até \(t-1\)) para uso como previsão de verdade.
- Expor o regime atual numa API (FastAPI), com Docker e deploy.