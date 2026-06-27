import { useQuery } from "@tanstack/react-query"
import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

import { getMonthly } from "../api/client"
import type { MonthlyPoint } from "../types"

export function MonthlyChart() {
  const { data } = useQuery<MonthlyPoint[]>({
    queryKey: ["monthly"],
    queryFn: getMonthly,
  })
  if (!data) return <p>Загрузка…</p>
  return (
    <section>
      <h2>Динамика по месяцам</h2>
      <ComposedChart width={640} height={320} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="income" name="Доход" fill="#7ed321" />
        <Bar dataKey="expense" name="Расход" fill="#d0021b" />
        <Line
          type="monotone"
          dataKey="running_balance"
          name="Накоплено"
          stroke="#4c9aff"
        />
      </ComposedChart>
    </section>
  )
}
