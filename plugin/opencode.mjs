/** PentaPRO OpenCode V2 adapter. No hooks, filesystem writes or model calls. */
import { readFile, realpath } from "node:fs/promises"
import { fileURLToPath } from "node:url"
import { dirname, resolve, relative, isAbsolute } from "node:path"

const root = dirname(dirname(fileURLToPath(import.meta.url)))
export async function loadSkills(directory = root) {
 const base = await realpath(directory)
 const catalog = JSON.parse(await readFile(resolve(base, "plugin/catalog.json"), "utf8"))
 const seen = new Set()
 const skills = []
 for (const entry of catalog) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(entry.id) || seen.has(entry.id)) throw new Error("Invalid or duplicate PentaPRO skill ID")
  seen.add(entry.id)
  const path = await realpath(resolve(base, entry.path))
  const location = relative(base, path)
  if (location.startsWith("..") || isAbsolute(location)) throw new Error("PentaPRO skill path escapes plugin")
  const source = await readFile(path, "utf8")
  if (!source.startsWith("---\n")) throw new Error(`Missing frontmatter: ${entry.id}`)
  const end = source.indexOf("\n---\n", 4)
  if (end < 0) throw new Error(`Invalid frontmatter: ${entry.id}`)
  skills.push({ id: entry.id, name: entry.id, description: entry.description, path, content: source.slice(end + 5), autoinvoke: entry.autoinvoke !== false })
 }
 return skills
}
export async function setup(ctx) {
 if (typeof ctx?.skill?.transform !== "function") throw new Error("PentaPRO requires the OpenCode V2 skill.transform API; use npx skills add on older clients")
 const skills = await loadSkills()
 const registration = await ctx.skill.transform(editor => {
  // Existing project/user definitions win. Never replace a customized skill.
  for (const skill of skills) if (!editor.get(skill.id)) editor.add(skill)
 })
 return async () => { await registration.dispose() }
}
export default { id: "pentapro", setup }
