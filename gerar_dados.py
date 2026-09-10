import random
from datetime import datetime, timedelta

import pandas as pd


random.seed(42)


restaurantes = [
    "Sabor Nordestino",
    "Pizza Express",
    "Burger House",
    "Sushi Fortaleza",
    "Cantinho da Massa",
    "Churrasco & Cia",
    "Tempero Cearense",
    "Açaí Tropical",
]

categorias = [
    "Brasileira",
    "Pizza",
    "Hambúrguer",
    "Sushi",
    "Massas",
    "Churrasco",
    "Saudável",
    "Açaí",
]

cidades = [
    "Fortaleza",
    "Eusébio",
    "Caucaia",
    "Maracanaú",
]

metodos_pagamento = [
    "Cartão de crédito",
    "Cartão de débito",
    "Pix",
    "Dinheiro",
]

status_pedido = [
    "Entregue",
    "Cancelado",
]


pedidos = []

data_inicial = datetime(2026, 1, 1)

for pedido_id in range(1, 5001):

    data_pedido = data_inicial + timedelta(
        days=random.randint(0, 180)
    )

    hora = random.randint(10, 23)
    minuto = random.randint(0, 59)

    horario_pedido = f"{hora:02d}:{minuto:02d}"

    restaurante = random.choice(restaurantes)
    categoria = categorias[restaurantes.index(restaurante)]

    cidade = random.choice(cidades)

    valor_pedido = round(
        random.uniform(20, 180),
        2
    )

    tempo_entrega = random.randint(15, 70)

    avaliacao = random.randint(1, 5)

    metodo_pagamento = random.choice(
        metodos_pagamento
    )

    status = random.choices(
        status_pedido,
        weights=[95, 5],
        k=1
    )[0]

    pedidos.append(
        {
            "pedido_id": pedido_id,
            "data_pedido": data_pedido.strftime("%Y-%m-%d"),
            "horario_pedido": horario_pedido,
            "restaurante": restaurante,
            "categoria": categoria,
            "cidade": cidade,
            "valor_pedido": valor_pedido,
            "tempo_entrega_min": tempo_entrega,
            "avaliacao": avaliacao,
            "metodo_pagamento": metodo_pagamento,
            "status": status,
        }
    )


df = pd.DataFrame(pedidos)


df.loc[100, "avaliacao"] = None
df.loc[250, "tempo_entrega_min"] = None
df.loc[400, "cidade"] = None

df = pd.concat(
    [df, df.iloc[[50, 150, 300]]],
    ignore_index=True
)


df.to_csv(
    "data/pedidos.csv",
    index=False
)


print("Dataset criado com sucesso!")
print(f"Total de registros: {len(df)}")
print("Arquivo salvo em: data/pedidos.csv")