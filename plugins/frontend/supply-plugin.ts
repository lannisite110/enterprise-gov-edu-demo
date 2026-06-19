import type { RouteRecordRaw } from 'vue-router'

export interface LabPlugin {
  id: string
  title: string
  routePrefix: string
  routes: RouteRecordRaw[]
  apiBase: string
}

export const plugin: LabPlugin = {
  id: 'edu.cn.gov.supply',
  title: 'Supply Chain Ledger Demo',
  routePrefix: '/labs/edu.cn.gov.supply',
  routes: [{ path: '', component: () => import('./SupplyLab.vue') }],
  apiBase: '/api/v1/labs/edu.cn.gov.supply',
}

export default plugin
