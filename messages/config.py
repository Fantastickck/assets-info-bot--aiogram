import emoji


CMD_EMOJI = {
    'general_info': f'{emoji.emojize(":open_book:")} Общая Информация',
    'charts': f'{emoji.emojize(":chart_increasing:")} Графики',
    'last_price': f'{emoji.emojize(":dollar_banknote:")} Последняя Цена',
    'fundamentals': f'{emoji.emojize(":magnifying_glass_tilted_left:")} Фундаментальные Показатели',
    'change_asset_type': '🔄 Изменить Тип Инструмента',
}

ASSET_EMOJI = {
    'share': f'{emoji.emojize(":scroll:")} Акция',
    'etf': f'{emoji.emojize(":classical_building:")}  ETF',
    'crypto': f'{emoji.emojize(":desktop_computer:")}  Криптовалюта',
}
