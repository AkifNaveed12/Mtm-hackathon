import { Button } from '@/components/ui/button'
import {
Dialog,
DialogContent,
DialogDescription,
DialogFooter,
DialogHeader,
DialogTitle,
DialogTrigger
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { LogInIcon } from 'lucide-react'

const DialogSignInDemo = () => {
return (

<Dialog>
<form>
<DialogTrigger render={<Button variant='outline' />}>Sign In</DialogTrigger>
<DialogContent className='to-card bg-linear-to-b from-sky-100 to-40% bg-size-[100%_101%] dark:from-sky-900'>
<DialogHeader className='items-center'>
<div className='mb-4 flex size-12 items-center justify-center rounded-full bg-sky-600/10 sm:mx-0 dark:bg-sky-400/10'>
<LogInIcon className='size-6 text-sky-600 dark:text-sky-400' />
</div>
<DialogTitle>Sign in with email</DialogTitle>
<DialogDescription className='text-center'>
Make a new doc to bring your words, data and teams together. For free.
</DialogDescription>
</DialogHeader>
<form className='flex flex-col gap-4'>
<div className='grid gap-3'>
<Label htmlFor='email'>Email</Label>
<Input type='email' id='email' name='useremail' placeholder='example@gmail.com' />
</div>
<div className='grid gap-3'>
<Label htmlFor='password'>Password</Label>
<Input type='password' id='password' name='userpassword' placeholder='Password' />
</div>
</form>
<DialogFooter className='flex-col! space-y-2 pt-4'>
<Button className='bg-sky-600 text-white hover:bg-sky-600 focus-visible:ring-sky-600 dark:bg-sky-400 dark:hover:bg-sky-400 dark:focus-visible:ring-sky-400'>
Get Started
</Button>
<div className='before:bg-border after:bg-border flex items-center gap-4 before:h-px before:flex-1 after:h-px after:flex-1'>
<span className='text-muted-foreground text-xs'>Or sign in with</span>
</div>
<div className='flex flex-wrap items-center justify-center gap-4'>
<Button variant='outline' className='flex-1'>
<img
                  src='https://cdn.shadcnstudio.com/ss-assets/brand-logo/google-icon.png?width=20&height=20&format=auto'
                  alt='Google Icon'
                  className='size-5'
                />
</Button>
<Button variant='outline' className='flex-1'>
<img
                  src='https://cdn.shadcnstudio.com/ss-assets/brand-logo/twitter-icon.png?width=20&height=20&format=auto'
                  alt='X Icon'
                  className='size-5 dark:invert'
                />
</Button>
<Button variant='outline' className='flex-1'>
<img
                  src='https://cdn.shadcnstudio.com/ss-assets/brand-logo/facebook-icon.png?width=20&height=20&format=auto'
                  alt='Facebook Icon'
                  className='size-5'
                />
</Button>
<Button variant='outline' className='flex-1'>
<img
                  src='https://cdn.shadcnstudio.com/ss-assets/brand-logo/github-icon.png?width=20&height=20&format=auto'
                  alt='GitHub Icon'
                  className='size-5 dark:invert'
                />
</Button>
</div>
</DialogFooter>
</DialogContent>
</form>
</Dialog>
)
}

export default DialogSignInDemo

npx shadcn@latest add @ss-components/data-table-01

'use client'

import { useState } from 'react'

import type { ColumnDef, ColumnFiltersState, SortingState, VisibilityState } from '@tanstack/react-table'
import {
flexRender,
getCoreRowModel,
getFilteredRowModel,
getPaginationRowModel,
getSortedRowModel,
useReactTable
} from '@tanstack/react-table'

import { Checkbox } from '@/components/ui/checkbox'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

const data: Payment[] = [
{
id: '1',
name: 'Shang Chain',
amount: 699,
status: 'success',
email: 'shang07@yahoo.com'
},
{
id: '2',
name: 'Kevin Lincoln',
amount: 242,
status: 'success',
email: 'kevinli09@gmail.com'
},
{
id: '3',
name: 'Milton Rose',
amount: 655,
status: 'processing',
email: 'rose96@gmail.com'
},
{
id: '4',
name: 'Silas Ryan',
amount: 874,
status: 'success',
email: 'silas22@gmail.com'
},
{
id: '5',
name: 'Ben Tenison',
amount: 541,
status: 'failed',
email: 'bent@hotmail.com'
}
]

export type Payment = {
id: string
name: string
amount: number
status: 'pending' | 'processing' | 'success' | 'failed'
email: string
}

export const columns: ColumnDef<Payment>[] = [
{
id: 'select',
header: ({ table }) => (
<Checkbox
checked={table.getIsAllPageRowsSelected()}
indeterminate={table.getIsSomePageRowsSelected()}
onCheckedChange={value => table.toggleAllPageRowsSelected(!!value)}
aria-label='Select all'
/>
),
cell: ({ row }) => (
<Checkbox
checked={row.getIsSelected()}
onCheckedChange={value => row.toggleSelected(!!value)}
aria-label='Select row'
/>
),
enableSorting: false,
enableHiding: false
},
{
accessorKey: 'name',
header: 'Name',
cell: ({ row }) => <div className='font-medium'>{row.getValue('name')}</div>
},
{
accessorKey: 'status',
header: 'Status',
cell: ({ row }) => <div className='capitalize'>{row.getValue('status')}</div>
},
{
accessorKey: 'email',
header: 'Email',
cell: ({ row }) => <div className='lowercase'>{row.getValue('email')}</div>
},
{
accessorKey: 'amount',
header: () => <div className='text-right'>Amount</div>,
cell: ({ row }) => {
const amount = parseFloat(row.getValue('amount'))

      const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(amount)

      return <div className='text-right font-medium'>{formatted}</div>
    }

}
]

const DataTableDemo = () => {
const [sorting, setSorting] = useState<SortingState>([])
const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({})
const [rowSelection, setRowSelection] = useState({})

const table = useReactTable({
data,
columns,
onSortingChange: setSorting,
onColumnFiltersChange: setColumnFilters,
getCoreRowModel: getCoreRowModel(),
getPaginationRowModel: getPaginationRowModel(),
getSortedRowModel: getSortedRowModel(),
getFilteredRowModel: getFilteredRowModel(),
onColumnVisibilityChange: setColumnVisibility,
onRowSelectionChange: setRowSelection,
state: {
sorting,
columnFilters,
columnVisibility,
rowSelection
}
})

return (
<div className='w-full'>
<div className='rounded-md border'>
<Table>
<TableHeader>
{table.getHeaderGroups().map(headerGroup => (
<TableRow key={headerGroup.id}>
{headerGroup.headers.map(header => {
return (
<TableHead key={header.id}>
{header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
</TableHead>
)
})}
</TableRow>
))}
</TableHeader>
<TableBody>
{table.getRowModel().rows?.length ? (
table.getRowModel().rows.map(row => (
<TableRow key={row.id} data-state={row.getIsSelected() && 'selected'}>
{row.getVisibleCells().map(cell => (
<TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
))}
</TableRow>
))
) : (
<TableRow>
<TableCell colSpan={columns.length} className='h-24 text-center'>
No results.
</TableCell>
</TableRow>
)}
</TableBody>
</Table>
</div>
<p className='text-muted-foreground mt-4 text-center text-sm'>Default data table</p>
</div>
)
}

export default DataTableDemo
