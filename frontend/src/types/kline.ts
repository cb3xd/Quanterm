export interface KlinePacket {
  exchangeId: string;
  symbol: string;
  interval: string;
  openPrice: string;
  closePrice: string;
  highPrice: string;
  lowPrice: string;
  volume: string;
  trades: number;
  isClosed: boolean;
  quoteVolume: string;
  takerBuyBaseVolume: string;
  takerBuyQuoteVolume: string;
  eventId: string;
}
