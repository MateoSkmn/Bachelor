import { Component, ElementRef, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../global/header/header.component';
import { StyledButtonComponent } from '../../global/styled-button/styled-button.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [HeaderComponent, StyledButtonComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

  @ViewChild('fileInput') fileInput!: ElementRef;

  uploadFile(): void {
    this.fileInput.nativeElement.click();
  }

  handleFileInput(event: any): void {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    // TODO: Use Service to upload file
    console.log(file);
  }
}
