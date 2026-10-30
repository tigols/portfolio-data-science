SELECT
  data,
  valor,
  valor - LAG(valor) OVER (ORDER BY data) AS variacao
FROM bcb_usd_ptax
ORDER BY data;