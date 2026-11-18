npx shadcn@latest add @ss-components/table-04

import {
Table,
TableBody,
TableCaption,
TableCell,
TableFooter,
TableHead,
TableHeader,
TableRow
} from '@/components/ui/table'

const invoices = [
{
invoice: 'INV001',
paymentStatus: 'Paid',
totalAmount: '$250.00',
paymentMethod: 'Credit Card'
},
{
invoice: 'INV002',
paymentStatus: 'Pending',
totalAmount: '$150.00',
paymentMethod: 'PayPal'
},
{
invoice: 'INV003',
paymentStatus: 'Unpaid',
totalAmount: '$350.00',
paymentMethod: 'Bank Transfer'
},
{
invoice: 'INV004',
paymentStatus: 'Paid',
totalAmount: '$450.00',
paymentMethod: 'Credit Card'
},
{
invoice: 'INV005',
paymentStatus: 'Paid',
totalAmount: '$550.00',
paymentMethod: 'PayPal'
},
{
invoice: 'INV006',
paymentStatus: 'Pending',
totalAmount: '$200.00',
paymentMethod: 'Bank Transfer'
},
{
invoice: 'INV007',
paymentStatus: 'Unpaid',
totalAmount: '$300.00',
paymentMethod: 'Credit Card'
}
]

const TableWithVerticalLinesDemo = () => {
return (
<Table>
<TableCaption>Table with vertical lines.</TableCaption>
<TableHeader>
<TableRow className='*:border-border [&>:not(:last-child)]:border-r'>
<TableHead className='w-25'>Invoice</TableHead>
<TableHead>Status</TableHead>
<TableHead>Method</TableHead>
<TableHead className='text-right'>Amount</TableHead>
</TableRow>
</TableHeader>
<TableBody>
{invoices.map(invoice => (
<TableRow key={invoice.invoice} className='*:border-border [&>:not(:last-child)]:border-r'>
<TableCell className='font-medium'>{invoice.invoice}</TableCell>
<TableCell>{invoice.paymentStatus}</TableCell>
<TableCell>{invoice.paymentMethod}</TableCell>
<TableCell className='text-right'>{invoice.totalAmount}</TableCell>
</TableRow>
))}
</TableBody>
<TableFooter>
<TableRow>
<TableCell colSpan={3}>Total</TableCell>
<TableCell className='text-right'>$2,500.00</TableCell>
</TableRow>
</TableFooter>
</Table>
)
}

export default TableWithVerticalLinesDemo

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add table
```

Copy-paste this file to `components/shadcn-studio/table` folder:

```tsx
table-04.tsx
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table'

const invoices = [
  {
    invoice: 'INV001',
    paymentStatus: 'Paid',
    totalAmount: '$250.00',
    paymentMethod: 'Credit Card'
  },
  {
    invoice: 'INV002',
    paymentStatus: 'Pending',
    totalAmount: '$150.00',
    paymentMethod: 'PayPal'
  },
  {
    invoice: 'INV003',
    paymentStatus: 'Unpaid',
    totalAmount: '$350.00',
    paymentMethod: 'Bank Transfer'
  },
  {
    invoice: 'INV004',
    paymentStatus: 'Paid',
    totalAmount: '$450.00',
    paymentMethod: 'Credit Card'
  },
  {
    invoice: 'INV005',
    paymentStatus: 'Paid',
    totalAmount: '$550.00',
    paymentMethod: 'PayPal'
  },
  {
    invoice: 'INV006',
    paymentStatus: 'Pending',
    totalAmount: '$200.00',
    paymentMethod: 'Bank Transfer'
  },
  {
    invoice: 'INV007',
    paymentStatus: 'Unpaid',
    totalAmount: '$300.00',
    paymentMethod: 'Credit Card'
  }
]

const TableWithVerticalLinesDemo = () => {
  return (
    <Table>
      <TableCaption>Table with vertical lines.</TableCaption>
      <TableHeader>
        <TableRow className='*:border-border [&>:not(:last-child)]:border-r'>
          <TableHead className='w-25'>Invoice</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Method</TableHead>
          <TableHead className='text-right'>Amount</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {invoices.map(invoice => (
          <TableRow key={invoice.invoice} className='*:border-border [&>:not(:last-child)]:border-r'>
            <TableCell className='font-medium'>{invoice.invoice}</TableCell>
            <TableCell>{invoice.paymentStatus}</TableCell>
            <TableCell>{invoice.paymentMethod}</TableCell>
            <TableCell className='text-right'>{invoice.totalAmount}</TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={3}>Total</TableCell>
          <TableCell className='text-right'>$2,500.00</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  )
}

export default TableWithVerticalLinesDemo
```

Instructions to follow:

- Install all listed dependencies and devDependencies using package manager used in the project (npm, yarn, pnpm, etc.)
- Install the required shadcn/ui components using the shadcn CLI using package manager used in the project (npx, pnpm dlx, bunx --bun, etc.)
- Add any CSS variables and styles to the `globals.css` file of this project (just add styles that are listed, no need to add extra styles or variables)
- Create the files with the exact paths provided
- Ensure all imports are correctly configured
- The component should be fully functional and styled according to the provided code
- Now you can use this component in current project

Important: File paths for components, utils, ui, lib, and hooks may vary depending on the project structure. Always check the project's `components.json` file to determine the correct import paths and folder structure. Update all import statements and file paths in the provided code to match the project's configuration before implementing the component.
