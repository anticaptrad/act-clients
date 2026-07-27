export interface HealthResponse {
  status: string;
}

export interface ReadyResponse {
  ready: boolean;
  nats_connected?: boolean;
  database_connected?: boolean;
}

export declare class ActHttpError extends Error {
  readonly status: number;
  readonly body: string;
  constructor(status: number, body: string);
}

export declare class ActClient {
  constructor(baseUrl: string | URL);
  health(): Promise<HealthResponse>;
  ready(): Promise<ReadyResponse>;
}
