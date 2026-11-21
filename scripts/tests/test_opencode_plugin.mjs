import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, mkdir, writeFile, symlink, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import plugin, { loadSkills, setup } from '../../plugin/opencode.mjs'

test('loads all 24 canonical skills with real resource paths', async () => {
 const skills = await loadSkills()
 assert.equal(skills.length, 24)
 assert.equal(new Set(skills.map(s => s.id)).size, 24)
 for (const skill of skills) { assert.ok(skill.content.trim()); assert.ok(skill.path.endsWith('/SKILL.md')); assert.ok(!skill.content.startsWith('---\n')) }
 assert.equal(plugin.id, 'pentapro')
})
test('keeps customized skills and disposes only its registration', async () => {
 const existing = { id: 'git-ship', content: 'customized' }
 const entries = new Map([['git-ship', existing]])
 let disposed = false
 const cleanup = await setup({skill:{transform: async callback => { callback({get:id=>entries.get(id),add:s=>entries.set(s.id,s)}); return {dispose:async()=>{ disposed=true }} }}})
 assert.equal(entries.size,24); assert.equal(entries.get('git-ship'),existing)
 await cleanup(); assert.equal(disposed,true)
})
test('older runtimes get an actionable error before any effect', async () => {
 await assert.rejects(setup({}), /OpenCode V2.*npx skills add/)
})
test('rejects escaping paths and duplicate IDs before registration', async () => {
 const root = await mkdtemp(join(tmpdir(),'pentapro-plugin-test-'))
 try {
  await mkdir(join(root,'plugin')); await writeFile(join(root,'outside.md'),'---\nname: x\n---\nBody')
  await symlink(join(root,'outside.md'),join(root,'linked.md'))
  await writeFile(join(root,'plugin/catalog.json'),JSON.stringify([{id:'x',path:'../outside.md'}]))
  await assert.rejects(loadSkills(root))
  await writeFile(join(root,'plugin/catalog.json'),JSON.stringify([{id:'x',path:'outside.md'},{id:'x',path:'outside.md'}]))
  await assert.rejects(loadSkills(root), /duplicate/)
 } finally {await rm(root,{recursive:true,force:true})}
})
