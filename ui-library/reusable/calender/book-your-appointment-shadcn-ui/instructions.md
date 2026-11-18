npx shadcn@latest add @ss-components/calendar-24

'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { CircleCheckIcon } from 'lucide-react'

const CalendarAppointmentBookingDemo = () => {
const [date, setDate] = useState<Date | undefined>(new Date(2025, 5, 20))
const [selectedTime, setSelectedTime] = useState<string | null>('10:00')

const timeSlots = Array.from({ length: 37 }, (\_, i) => {
const totalMinutes = i \* 15
const hour = Math.floor(totalMinutes / 60) + 9
const minute = totalMinutes % 60

    return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`

})

const bookedDates = Array.from({ length: 3 }, (\_, i) => new Date(2025, 5, 17 + i))

return (

<div>
<Card className='gap-0 p-0'>
<CardHeader className='flex h-max justify-center border-b p-4!'>
<CardTitle>Book your appointment</CardTitle>
</CardHeader>
<CardContent className='relative p-0 md:pr-48'>
<div className='p-6 max-sm:flex max-sm:justify-center'>
<Calendar
mode='single'
selected={date}
onSelect={setDate}
defaultMonth={date}
disabled={bookedDates}
showOutsideDays={false}
modifiers={{
                booked: bookedDates
              }}
modifiersClassNames={{
                booked: '[&>button]:line-through opacity-100'
              }}
className='bg-transparent p-0 [--cell-size:--spacing(10)]'
formatters={{
                formatWeekdayName: date => {
                  return date.toLocaleString('en-US', { weekday: 'short' })
                }
              }}
/>
</div>
<div className='inset-y-0 right-0 flex w-full flex-col gap-4 border-t max-md:h-60 md:absolute md:w-48 md:border-t-0 md:border-l'>
<ScrollArea className='h-full'>
<div className='flex flex-col gap-2 p-6'>
{timeSlots.map(time => (
<Button
key={time}
variant={selectedTime === time ? 'default' : 'outline'}
onClick={() => setSelectedTime(time)}
className='w-full shadow-none' >
{time}
</Button>
))}
</div>
</ScrollArea>
</div>
</CardContent>
<CardFooter className='flex flex-col gap-4 border-t px-6 py-5! md:flex-row'>
<div className='flex items-center gap-2 text-sm'>
{date && selectedTime ? (
<>
<CircleCheckIcon className='size-5 stroke-green-600 dark:stroke-green-400' />
<span>
Your meeting is booked for{' '}
<span className='font-medium'>
{' '}
{date?.toLocaleDateString('en-US', {
weekday: 'long',
day: 'numeric',
month: 'long'
})}{' '}
</span>
at <span className='font-medium'>{selectedTime}</span>.
</span>
</>
) : (
<>Select a date and time for your meeting.</>
)}
</div>
<Button disabled={!date || !selectedTime} className='w-full md:ml-auto md:w-auto' variant='outline'>
Continue
</Button>
</CardFooter>
</Card>
<p className='text-muted-foreground mt-4 text-center text-xs' role='region'>
Appointment calendar
</p>
</div>
)
}

export default CalendarAppointmentBookingDemo
Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button calendar card scroll-area
```

Copy-paste this file to `components/shadcn-studio/calendar` folder:

```tsx
calendar-24.tsx
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Calendar } from '@/components/ui/calendar'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
import { CircleCheckIcon } from 'lucide-react'

const CalendarAppointmentBookingDemo = () => {
  const [date, setDate] = useState<Date | undefined>(new Date(2025, 5, 20))
  const [selectedTime, setSelectedTime] = useState<string | null>('10:00')

  const timeSlots = Array.from({ length: 37 }, (_, i) => {
    const totalMinutes = i * 15
    const hour = Math.floor(totalMinutes / 60) + 9
    const minute = totalMinutes % 60

    return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`
  })

  const bookedDates = Array.from({ length: 3 }, (_, i) => new Date(2025, 5, 17 + i))

  return (
    <div>
      <Card className='gap-0 p-0'>
        <CardHeader className='flex h-max justify-center border-b p-4!'>
          <CardTitle>Book your appointment</CardTitle>
        </CardHeader>
        <CardContent className='relative p-0 md:pr-48'>
          <div className='p-6 max-sm:flex max-sm:justify-center'>
            <Calendar
              mode='single'
              selected={date}
              onSelect={setDate}
              defaultMonth={date}
              disabled={bookedDates}
              showOutsideDays={false}
              modifiers={{
                booked: bookedDates
              }}
              modifiersClassNames={{
                booked: '[&>button]:line-through opacity-100'
              }}
              className='bg-transparent p-0 [--cell-size:--spacing(10)]'
              formatters={{
                formatWeekdayName: date => {
                  return date.toLocaleString('en-US', { weekday: 'short' })
                }
              }}
            />
          </div>
          <div className='inset-y-0 right-0 flex w-full flex-col gap-4 border-t max-md:h-60 md:absolute md:w-48 md:border-t-0 md:border-l'>
            <ScrollArea className='h-full'>
              <div className='flex flex-col gap-2 p-6'>
                {timeSlots.map(time => (
                  <Button
                    key={time}
                    variant={selectedTime === time ? 'default' : 'outline'}
                    onClick={() => setSelectedTime(time)}
                    className='w-full shadow-none'
                  >
                    {time}
                  </Button>
                ))}
              </div>
            </ScrollArea>
          </div>
        </CardContent>
        <CardFooter className='flex flex-col gap-4 border-t px-6 py-5! md:flex-row'>
          <div className='flex items-center gap-2 text-sm'>
            {date && selectedTime ? (
              <>
                <CircleCheckIcon className='size-5 stroke-green-600 dark:stroke-green-400' />
                <span>
                  Your meeting is booked for{' '}
                  <span className='font-medium'>
                    {' '}
                    {date?.toLocaleDateString('en-US', {
                      weekday: 'long',
                      day: 'numeric',
                      month: 'long'
                    })}{' '}
                  </span>
                  at <span className='font-medium'>{selectedTime}</span>.
                </span>
              </>
            ) : (
              <>Select a date and time for your meeting.</>
            )}
          </div>
          <Button disabled={!date || !selectedTime} className='w-full md:ml-auto md:w-auto' variant='outline'>
            Continue
          </Button>
        </CardFooter>
      </Card>
      <p className='text-muted-foreground mt-4 text-center text-xs' role='region'>
        Appointment calendar
      </p>
    </div>
  )
}

export default CalendarAppointmentBookingDemo
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
