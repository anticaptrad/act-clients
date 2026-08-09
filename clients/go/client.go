package actclient

import (
 "context"
 "encoding/json"
 "fmt"
 "net/http"
 "strings"
)

type Client struct { BaseURL string; HTTP *http.Client }
func New(baseURL string) *Client { return &Client{BaseURL: strings.TrimRight(baseURL, "/"), HTTP: http.DefaultClient} }
func (c *Client) get(ctx context.Context, path string) (map[string]any, error) { req, err := http.NewRequestWithContext(ctx, http.MethodGet, c.BaseURL+path, nil); if err != nil { return nil, err }; req.Header.Set("Accept", "application/json"); res, err := c.HTTP.Do(req); if err != nil { return nil, err }; defer res.Body.Close(); if res.StatusCode < 200 || res.StatusCode >= 300 { return nil, fmt.Errorf("act API returned HTTP %d", res.StatusCode) }; var out map[string]any; if err := json.NewDecoder(res.Body).Decode(&out); err != nil { return nil, err }; return out, nil }
func (c *Client) Health(ctx context.Context) (map[string]any, error) { return c.get(ctx, "/health") }
func (c *Client) Ready(ctx context.Context) (map[string]any, error) { return c.get(ctx, "/ready") }
