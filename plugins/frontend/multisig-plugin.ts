import type { RouteRecordRaw } from 'vue-router'

export interface LabPlugin {
  id: string
  title: string
  routePrefix: string
  routes: RouteRecordRaw[]
  apiBase: string
}

export const plugin: LabPlugin = {
  id: 'edu.cn.gov.multisig',
  title: 'Multisig Approval Demo',
  routePrefix: '/labs/edu.cn.gov.multisig',
  routes: [{ path: '', component: () => import('./MultisigLab.vue') }],
  apiBase: '/api/v1/labs/edu.cn.gov.multisig',
}

export default plugin
