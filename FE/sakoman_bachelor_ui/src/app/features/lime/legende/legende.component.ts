import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { StyledButtonComponent } from '../../../global/components/styled-button/styled-button.component';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-legende',
  standalone: true,
  imports: [StyledButtonComponent, MatIconModule],
  templateUrl: './legende.component.html',
  styleUrl: './legende.component.scss'
})
export class LegendeComponent {
  constructor(public dialogRef: MatDialogRef<LegendeComponent>) {}

  colorLegende= [
    {color: 'green', value: 5},
    {color: 'lime', value: 4},
    {color: 'yellow', value: 3},
    {color: 'orange', value: 2},
    {color: 'red', value: 1},
  ]

  /**
   * Closes the dialog
   */
  closeLegende(): void {
    this.dialogRef.close();
  }
}
