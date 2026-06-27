import { useQuery } from "@tanstack/react-query"
import { Cell, Legend, Pie, PieChart, Tooltip } from "recharts"

import { getByCategory } from "../api/client"
import type { CategoryAmount } from "../types"

const COLORS = ["#4c9aff", "#f5a623", "#7ed321", "#d0021b", "#9013fe", "#50e3c2"]

export function CategoryPie() {
  const { data } = useQuery<CategoryAmount[]>({
    queryKey: ["by-category"],
    queryFn: getByCategory,
  })
  if (!data) return <p>Загрузка…</p>
  return (
    <section>
      <h2>Расходы по категориям</h2>
      <PieChart width={360} height={300}>
        <Pie
          data={data}
          dataKey="total"
          nameKey="category"
          cx="50%"
          cy="50%"
          outerRadius={100}
          label
        >
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </section>
  )
}
