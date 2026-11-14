try:
 import tomllib
except ModuleNotFoundError:
 tomllib=None
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CodexContract(unittest.TestCase):
 def test_project_config_is_http_oauth_without_inline_secrets(self):
  cfg_path=ROOT/".codex/config.toml"
  cfg=cfg_path.read_text()
  if tomllib:
   parsed=tomllib.loads(cfg)
   self.assertEqual(parsed["mcp_servers"]["weavz"]["url"],"https://platform.weavz.io/mcp/weavz")
   self.assertTrue(parsed["mcp_servers"]["weavz"]["enabled"])
  else:
   in_server=False
   values={}
   for line in cfg.splitlines():
    line=line.strip()
    if line.startswith("["):
     in_server=line=="[mcp_servers.weavz]"
    elif in_server and "=" in line:
     key,value=(part.strip() for part in line.split("=",1))
     values[key]=value.strip('"')
   self.assertEqual(values.get("url"),"https://platform.weavz.io/mcp/weavz")
   self.assertEqual(values.get("enabled"),"true")
  self.assertIn('[mcp_servers.weavz]',cfg)
  self.assertIn('url = "https://platform.weavz.io/mcp/weavz"',cfg)
  self.assertIn('enabled = true',cfg)
  self.assertNotIn('Authorization',cfg); self.assertNotIn('token',cfg.lower())
 def test_project_guidance(self):
  self.assertIn('MCP setup is client configuration',(ROOT/"AGENTS.md").read_text())
if __name__=='__main__': unittest.main()
